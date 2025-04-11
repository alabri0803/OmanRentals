# Generated by Django 5.2 on 2025-04-11 18:32

import django.core.validators
import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_gender_alter_customuser_omani_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': '🏢 شركة', 'verbose_name_plural': '🏢 الشركات'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-date_joined'], 'verbose_name': '👤 مستخدم', 'verbose_name_plural': '👥 المستخدمين'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '📝 ملف شخصي', 'verbose_name_plural': '📂 الملفات الشخصية'},
        ),
        migrations.RemoveField(
            model_name='company',
            name='tax_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='national_id',
        ),
        migrations.AlterField(
            model_name='company',
            name='commercial_license',
            field=models.CharField(help_text='مثال: 12345/2023', max_length=50, validators=[users.validators.validate_commercial_license], verbose_name='📜 السجل التجاري'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name_ar',
            field=models.CharField(max_length=100, verbose_name='🏢 اسم الشركة (عربي)'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name_en',
            field=models.CharField(max_length=100, verbose_name='🏢 اسم الشركة (إنجليزي)'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='✅ موثوق'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='omani_id',
            field=models.CharField(blank=True, help_text='مثال: 1234567', max_length=20, validators=[users.validators.validate_omani_id], verbose_name='🆔 الهوية العمانية'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(help_text='يجب أن يبدأ بـ +968 ويتبعه 8 أرقام', max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='رقم هاتف غير صحيح! مثال: +96812345678', regex='^\\+968\\d{8}$')], verbose_name='📱 رقم الهاتف'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('OWNER', '👑 مالك العقار'), ('INVESTOR', '💼 مستثمر'), ('TENANT', '🏠 مستأجر'), ('COMPANY', '🏢 شركة')], default='TENANT', max_length=10, verbose_name='👥 نوع المستخدم'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_ar',
            field=models.TextField(blank=True, verbose_name='🏠 العنوان (عربي)'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_en',
            field=models.TextField(blank=True, verbose_name='🏠 العنوان (إنجليزي)'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', '👨 ذكر'), ('F', '👩 أنثى'), ('O', '🧑 أخرى')], max_length=1, verbose_name='🚻 الجنس'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='users/profiles/', verbose_name='📷 صورة الملف'),
        ),
    ]
