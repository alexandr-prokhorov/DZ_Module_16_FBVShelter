from django.db import models

from users.models import NULLABLE

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name='Порода')
    description = models.CharField(max_length=1000, verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'

class Dog(models.Model):
    name = models.CharField(max_length=250, verbose_name='Кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода')
    photo = models.ImageField(upload_to='dogs/', **NULLABLE, verbose_name='Фото')
    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения')

    def __str__(self):
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