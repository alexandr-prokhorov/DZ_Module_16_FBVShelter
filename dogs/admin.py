from django.contrib import admin

from dogs.models import Breed, Dog


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """
    Админский интерфейс для модели породы собак (Breed).
    Атрибуты:
    list_display (tuple): Поля, отображаемые в списке объектов породы.
    ordering (tuple): Порядок сортировки объектов породы по первичному ключу.
    """
    list_display = ('pk', 'name',)
    ordering = ('pk',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    """
    Админский интерфейс для модели собак (Dog).
    Атрибуты:
    list_display (tuple): Поля, отображаемые в списке объектов собак.
    list_filter (tuple): Поля, по которым можно фильтровать объекты собак.
    ordering (tuple): Порядок сортировки объектов собак по имени.
    """
    list_display = ('name', 'breed', 'owner')
    list_filter = ('breed',)
    ordering = ('name',)
