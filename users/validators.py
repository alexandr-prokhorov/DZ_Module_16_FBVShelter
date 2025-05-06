import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    """
    Проверяет, соответствует ли пароль заданным критериям.
    Пароль должен содержать только латинские буквы и цифры, а также иметь длину от 8 до 16 символов.
    Параметры:
    field: Пароль, который необходимо проверить.
    Исключения:
    ValidationError: Если пароль не соответствует критериям:
    - Содержит недопустимые символы (не латинские буквы и цифры).
    - Длина пароля не находится в диапазоне от 8 до 16 символов.
    """
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    language = settings.LANGUAGE_CODE
    error_messages = [
        {
            'ru-ru': 'Пароль должен содержать символы латинского алфавита и цифры',
            'en-us': 'MUST contain A-Z a-z letters and 0-9 numbers'
        },
        {
            'ru-ru': 'Пароль должен быть от 8 до 16 символов',
            'en-us': 'Password length must be between 8 and 16 charters'
        },
    ]
    if not bool(re.match(pattern, field)):
        print(error_messages[0][language])
        raise ValidationError(
            error_messages[0][language],
            code=error_messages[0][language]
        )
    if not 8 <= len(field) <= 16:
        print(error_messages[1][language])
        raise ValidationError(
            error_messages[1][language],
            code=error_messages[1][language]
        )
