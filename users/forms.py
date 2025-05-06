from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation


class StyleFormMixin:
    """
    Миксин для добавления стилей к полям формы.
    При инициализации добавляет класс 'form-control' ко всем полям формы,
    чтобы применить стили Bootstrap.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя.
    Позволяет пользователям создавать новый аккаунт с указанием email.
    Включает валидацию паролей.
    """
    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """
        Проверяет, совпадают ли оба введённых пароля.
        Возвращает:
        str: Второй пароль, если он валиден.
        Исключения:
        ValidationError: Если пароли не совпадают.
        """
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data['password1'])
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned_data['password2']


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма для входа пользователя.
    Позволяет пользователям вводить свои учетные данные для входа в систему.
    """
    pass


class UserForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для редактирования информации о пользователе.
    Позволяет пользователям обновлять свои данные, такие как email, имя и аватар.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')
        # exclude = ('is_active',)


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для обновления информации о пользователе.
    Позволяет пользователям изменять свои данные, включая email, имя и аватар.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    """
    Форма для изменения пароля пользователя.
    Позволяет пользователям изменять свой пароль с валидацией.
    """
    def clean_new_password2(self):
        """
        Проверяет, совпадают ли новые пароли и валидирует их.
        Возвращает:
        Новый пароль, если он валиден.
        Исключения:
        ValidationError: Если пароли не совпадают или не проходят валидацию.
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        password_validation.validate_password(password2, self.user)
        return password2
