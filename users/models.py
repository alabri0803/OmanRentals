from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
  class USER_TYPE_CHOICES(models.TextChoices):
    OWNER = 'OWNER', _('مالك العقار')
    INVESTOR = 'INVESTOR', _('مستثمر')
    TENANT = 'TENANT', _('مستأجر')
    COMPANY = 'COMPANY', _('شركة')
    
  phone_regex = RegexValidator(
      regex=r'^\+968\d{8}$',
      message=_("رقم الهاتف يجب أن يكون بالصيغة التالية: +968XXXXXXXX.")
    )
    # الحقول الأساسية
  user_type = models.CharField(
    max_length=10,
    choices=USER_TYPE_CHOICES.choices,
    default=USER_TYPE_CHOICES.TENANT,
    verbose_name=_('نوع المستخدم')
  )
  phone = models.CharField(
    max_length=15,
    validators=[phone_regex],
    unique=True,
    verbose_name=_('رقم الهاتف'),
  )
  is_verified = models.BooleanField(
    default=False,
    verbose_name=_('موثوق')
  )
  omani_id = models.CharField(
    max_length=20,
    blank=True,
    verbose_name=_('الهوية العمانية'),
    help_text=_('مثال: 1234567890123456')
  )

  class Meta:
    verbose_name = _('مستخدم')
    verbose_name_plural = _('المستخدمين')

  def __str__(self):
    return f"{self.username} ({self.get_user_type_display()})"

class UserProfile(models.Model):
  class Gender(models.TextChoices):
    MALE = 'M', _('ذكر')
    FEMALE = 'F', _('أنثى')
    
  user = models.OneToOneField(
    CustomUser, 
    on_delete=models.CASCADE,
    related_name='profile',
    verbose_name=_('المستخدم')
  )
  address_ar = models.TextField(
    verbose_name=_('العنوان بالعربية'),
    blank=True
  )
  address_en = models.TextField(
    verbose_name=_('العنوان بالإنجليزية'),
    blank=True
  )
  profile_picture = models.ImageField(
    upload_to='users/profiles/',
    verbose_name=_('صورة الملف الشخصي'),
    blank=True
  )
  national_id = models.CharField(
    max_length=20,
    blank=True,
    verbose_name=_('رقم الهوية الوطنية'),
  )
  gender = models.CharField(
    max_length=1,
    choices=Gender.choices,
    verbose_name=_('الجنس'),
    blank=True
  )

  class Meta:
    verbose_name = _('ملف الشخصي')
    verbose_name_plural = _('الملفات الشخصية')

class Company(models.Model):
  user = models.OneToOneField(
    CustomUser, 
    on_delete=models.CASCADE,
    related_name='company',
    verbose_name=_('المستخدم')
  )
  company_name_ar = models.CharField(
    max_length=100,
    verbose_name=_('اسم الشركة بالعربية')
  )
  company_name_en = models.CharField(
    max_length=100,
    verbose_name=_('اسم الشركة بالإنجليزية')
  )
  commercial_license = models.CharField(
    max_length=50,
    verbose_name=_('السجل التجاري'),
    help_text=_('مطلوب للشركات في عُمان')
  )
  tax_number = models.CharField(
    max_length=20,
    verbose_name=_('الرقم الضريبي'),
  )

  class Meta:
    verbose_name = _('شركة')
    verbose_name_plural = _('الشركات')