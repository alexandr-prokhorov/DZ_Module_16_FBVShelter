from django import forms
from reviews.models import Review
from users.forms import StyleFormMixin


class ReviewForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и редактирования отзывов (Review).
    Атрибуты формы:
    title: Заголовок отзыва.
    content: Текст отзыва.
    slug: Скрытое поле для уникального слага отзыва с начальным значением 'temp_slug'.
    Метаданные:
    model: Связанная модель Review.
    fields: Поля, включённые в форму.
    """
    title = forms.CharField(max_length=150, label='Заголовок')
    content = forms.TextInput()
    slug = forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ('dog', 'title', 'content', 'slug')
