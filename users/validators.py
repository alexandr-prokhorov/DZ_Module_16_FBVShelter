import re
from django.core.exceptions import ValidationError

def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    if not bool(re.match(pattern, field)):
        print('Пароль должен содержать латинские буквы и цифры')
        raise ValidationError('Пароль должен содержать латинские буквы и цифры')
    if not 8 <= len(field) <= 16:
        print('Пароль должен быть от 8 до 16 символов')
        raise ValidationError('Пароль должен быть от 8 до 16 символов')