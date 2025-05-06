from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    """
    Отправляет электронное письмо с подтверждением регистрации.
    Параметры:
    email: Адрес электронной почты пользователя, которому будет отправлено письмо.
    Отправляемое письмо содержит сообщение об успешной регистрации на платформе WEBCBVShelter.
    """
    send_mail(
        subject="Поздравляем с регистрацией на нашем сервисе",
        message="Вы успешно зарегистрировались на платформе WEBCBVShelter",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_new_password(email, new_password):
    """
    Отправляет электронное письмо с новым паролем.
    Параметры:
    email (str): Адрес электронной почты пользователя, которому будет отправлено письмо.
    new_password (str): Новый пароль, который будет отправлен пользователю.
    Отправляемое письмо содержит сообщение с новым паролем пользователя.
    """
    send_mail(
        subject="Вы успешно изменили пароль",
        message=f"Ваш новый пароль {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
