from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Админский интерфейс для модели отзывов (Review).
    Атрибуты:
    list_display: Поля, отображаемые в списке отзывов.
    ordering: Порядок сортировки отзывов (по дате создания).
    list_filter: Поля для фильтрации отзывов в админке.
    """
    list_display = ('title', 'dog', 'author', 'created', 'sign_of_review',)
    ordering = ('created',)
    list_filter = ('dog', 'author',)
