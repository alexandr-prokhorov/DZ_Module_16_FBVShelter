import datetime

from django import forms

from dogs.models import Dog, DogParent
from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для модели Dog с применением миксина стилей.
    Исключает из формы поля: owner, is_active, views.
    Методы:
    clean_birth_date: Валидирует поле даты рождения собаки,
    чтобы возраст собаки не превышал 35 лет.
    """

    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'views')

    def clean_birth_date(self):
        """
        Валидирует дату рождения собаки.
        Проверяет, что возраст собаки не превышает 35 лет.
        Если возраст больше 35 лет, выбрасывается ValidationError.
        Возвращает очищенное значение даты рождения.
        """
        cleaned_data = self.cleaned_data['birth_date']
        if cleaned_data:
            now_year = datetime.datetime.now().year
            if now_year - cleaned_data.year > 35:
                raise forms.ValidationError('Собака должна быть моложе 35 лет')
        return cleaned_data


class DogAdminForm(DogForm):
    """
    Форма для администрирования модели Dog, наследующая DogForm.
    Исключает из формы поле is_active.
    """

    class Meta(DogForm.Meta):
        exclude = ('is_active',)

    # def clean_birth_date(self):
    #     clean_birth_date = super().clean_birth_date()
    #     return clean_birth_date


class DogParentForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для модели DogParent с применением миксина стилей.
    Поля формы включают все поля модели DogParent.
    """
    class Meta:
        model = DogParent
        fields = '__all__'
