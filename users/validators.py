from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_omani_id(value):
    if not value.isdigit() or len(value) != 8:
        raise ValidationError(_('الهوية العمانية يجب أن تتكون من 8 أرقام!'))

def validate_commercial_license(value):
    if not all(char.isdigit() or char == '/' for char in value):
        raise ValidationError(_('صيغة السجل التجاري غير صالحة! مثال: 12345/2023'))