import string
import random


def slug_generator():
    """
    Генерирует случайный слаг длиной 20 символов.
    Слаг состоит из случайных букв нижнего и верхнего регистра, а также цифр.
    Возвращает:
    Случайно сгенерированный слаг длиной 20 символов.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
