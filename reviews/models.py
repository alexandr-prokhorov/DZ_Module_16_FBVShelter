from django.db import models
from django.conf import settings
from django.urls import reverse

from users.models import NULLABLE
from dogs.models import Dog


class Review(models.Model):
    """
    Модель для представления отзыва о собаке.
    Атрибуты:
    title: Заголовок отзыва (максимум 150 символов).
    slug: Уникальный слаг для URL (максимум 25 символов).
    content: Содержимое отзыва.
    created: Дата и время создания отзыва (автоматически устанавливается при создании).
    sign_of_review: Статус активности отзыва (по умолчанию True).
    author: Автор отзыва (ссылка на модель пользователя, может быть пустым).
    dog: Собака, к которой относится отзыв (ссылка на модель Dog).
    Методы:
    __str__(): Возвращает строковое представление отзыва (заголовок).
    get_absolute_url(): Возвращает URL для просмотра деталей отзыва.
    """
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержимое')
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    sign_of_review = models.BooleanField(default=True, verbose_name='Активный')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='dogs', verbose_name='Собака')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('reviews:review_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
