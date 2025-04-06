from django.db import models
from django.contrib.auth.models import  AbstractUser

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=150, verbose_name='first name', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='last name', default='Anonymous')
    phone = models.CharField(max_length=35, verbose_name='phone number', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='telegram username', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='active')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
