from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

def telephone_validator(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
    RegexValidator(regex=r'^\+?\d{9,15}$', message='Телефон должен содержать от 9 до 15 цифр')