from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """
    Класс для определения ролей пользователей.
    Используется для задания ролей (ADMIN, MODERATOR, USER) в модели User.
    """
    ADMIN = "admin", _('admin')
    MODERATOR = "moderator", _('moderator')
    USER = "user", _('user')


class User(AbstractUser):
    """
    Модель пользователя, расширяющая стандартную модель AbstractUser .
    Поля:
    email (EmailField): Уникальный адрес электронной почты пользователя.
    role (CharField): Роль пользователя (ADMIN, MODERATOR, USER).
    first_name (CharField): Имя пользователя.
    last_name (CharField): Фамилия пользователя.
    phone (CharField): Номер телефона пользователя (опционально).
    telegram (CharField): Telegram пользователя (опционально).
    avatar (ImageField): Аватар пользователя (опционально).
    is_active (BooleanField): Статус активности пользователя.
    Атрибуты:
    USERNAME_FIELD: Поле, используемое для аутентификации (email).
    REQUIRED_FIELDS: Список обязательных полей для создания пользователя.
    Методы:
    __str__(): Возвращает строковое представление пользователя (email).
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='Эл.Почта')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=150, verbose_name='Имя', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', default='Anonymous')
    phone = models.CharField(max_length=35, verbose_name='Номер Телефона', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='Телеграм', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
