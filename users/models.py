from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .validators import validate_omani_id, validate_commercial_license

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        OWNER = 'OWNER', _('👑 مالك العقار')
        INVESTOR = 'INVESTOR', _('💼 مستثمر')
        TENANT = 'TENANT', _('🏠 مستأجر')
        COMPANY = 'COMPANY', _('🏢 شركة')

    # تحقق من صحة رقم الهاتف العماني (يبدأ بـ +968)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^\+968\d{8}$', message=_('رقم هاتف غير صحيح! مثال: +96812345678'))],
        verbose_name=_('📱 رقم الهاتف'),
        help_text=_('يجب أن يبدأ بـ +968 ويتبعه 8 أرقام')
    )

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.TENANT,
        verbose_name=_('👥 نوع المستخدم')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('✅ موثوق')
    )
    omani_id = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_omani_id],
        verbose_name=_('🆔 الهوية العمانية'),
        help_text=_('مثال: 1234567')
    )

    class Meta:
        verbose_name = _('👤 مستخدم')
        verbose_name_plural = _('👥 المستخدمين')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', _('👨 ذكر')
        FEMALE = 'F', _('👩 أنثى')
        OTHER = 'O', _('🧑 أخرى')

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('المستخدم')
    )
    address_ar = models.TextField(
        verbose_name=_('🏠 العنوان (عربي)'),
        blank=True
    )
    address_en = models.TextField(
        verbose_name=_('🏠 العنوان (إنجليزي)'),
        blank=True
    )
    profile_picture = models.ImageField(
        upload_to='users/profiles/',
        verbose_name=_('📷 صورة الملف'),
        blank=True
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name=_('🚻 الجنس'),
        blank=True
    )

    class Meta:
        verbose_name = _('📝 ملف شخصي')
        verbose_name_plural = _('📂 الملفات الشخصية')


class Company(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='company',
        verbose_name=_('المستخدم')
    )
    company_name_ar = models.CharField(
        max_length=100,
        verbose_name=_('🏢 اسم الشركة (عربي)')
    )
    company_name_en = models.CharField(
        max_length=100,
        verbose_name=_('🏢 اسم الشركة (إنجليزي)')
    )
    commercial_license = models.CharField(
        max_length=50,
        validators=[validate_commercial_license],
        verbose_name=_('📜 السجل التجاري'),
        help_text=_('مثال: 12345/2023')
    )

    class Meta:
        verbose_name = _('🏢 شركة')
        verbose_name_plural = _('🏢 الشركات')