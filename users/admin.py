from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админский интерфейс для модели пользователей (User).
    Атрибуты:
    list_display (tuple): Поля, отображаемые в списке пользователей.
    list_filter (tuple): Поля для фильтрации пользователей в админке.
    """
    list_display = ('pk', 'email', 'last_name', 'first_name', 'is_active')
    list_filter = ('last_name',)
