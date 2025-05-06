from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from dogs.models import Breed


def get_breed_cache():
    """
    Получает список пород собак из кэша.
    Если кэш включен и список пород уже сохранен в кэше,
    возвращает его. В противном случае извлекает все породы
    из базы данных, сохраняет их в кэше и возвращает.
    Возвращает:
    QuerySet: Список всех пород собак.
    """
    if settings.CACHE_ENABLED:
        key = 'breed_list'
        breed_list = cache.get(key)
        if breed_list is None:
            breed_list = Breed.objects.all()
            cache.set(key, breed_list)
        else:
            breed_list = Breed.objects.all()

        return breed_list


def send_views_mail(dog_object, owner_email, views_count):
    """
    Отправляет электронное письмо владельцу собаки с информацией о количестве просмотров.
    Параметры:
    dog_object (Dog): Объект собаки, для которой отправляется уведомление.
    owner_email (str): Электронная почта владельца собаки.
    views_count (int): Количество просмотров профиля собаки.
    """
    send_mail(
        subject=f'{views_count} просмотров {dog_object}',
        message=f'Юхуу! Уже {views_count}, просмотров записи {dog_object}!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[owner_email, ]
    )
