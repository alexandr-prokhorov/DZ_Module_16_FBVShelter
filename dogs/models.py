from django.db import models
from django.conf import settings

from users.models import NULLABLE


class Breed(models.Model):
    """
    Модель для представления породы собак.
    Атрибуты:
    name (CharField): Название породы.
    description (CharField): Описание породы.
    """
    name = models.CharField(max_length=100, verbose_name='Порода')
    description = models.CharField(max_length=1000, verbose_name='Описание', **NULLABLE)

    def __str__(self):
        """
        Возвращает строковое представление породы.
        Возвращает:
        str: название породы.
        """
        return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    """
    Модель для представления собаки.
    Атрибуты:
    name (CharField): Кличка собаки.
    breed (ForeignKey): Порода собаки.
    photo (ImageField): Фото собаки.
    birth_date (DateField): Дата рождения собаки.
    is_active (BooleanField): Статус активности собаки.
    owner (ForeignKey): Хозяин собаки.
    views (IntegerField): Количество просмотров профиля собаки.
    """
    name = models.CharField(max_length=250, verbose_name='Кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода')
    photo = models.ImageField(upload_to='dogs/', **NULLABLE, verbose_name='Фото')
    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Хозяин')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        """
        Возвращает строковое представление собаки.
        Возвращает:
        str: Кличка и порода собаки.
        """
        return f'{self.name} ({self.breed})'

    class Meta:
        verbose_name = 'dog'
        verbose_name_plural = 'dogs'
        # варианты работы с мета классом
        # abstract = True
        # app_label = 'dogs'
        # ordering = [-1]
        # permissions = []
        # db_table = 'doggies'
        # get_latest_by = 'birth_date'

    def views_count(self):
        """
        Увеличивает количество просмотров профиля собаки на 1 и сохраняет изменения.
        """
        self.views += 1
        self.save()


class DogParent(models.Model):
    """
    Модель для представления родителя собаки.
    Атрибуты:
    dog (ForeignKey): Собака, к которой относится родитель.
    name (CharField): Кличка родителя.
    category (ForeignKey): Порода родителя.
    birthe_date (DateField): Дата рождения родителя.
    """
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Кличка Родителя')
    category = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода Родителя')
    birthe_date = models.DateField(**NULLABLE, verbose_name='Дата рождения Родителя')

    def __str__(self):
        """
        Возвращает строковое представление родителя.
        Возвращает:
        str: Кличка и порода родителя.
        """
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'parent'
        verbose_name_plural = 'parents'
