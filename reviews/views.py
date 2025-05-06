from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from reviews.forms import ReviewForm
from users.models import UserRoles
from reviews.utils import slug_generator


class ReviewListview(ListView):
    """
    Представление для отображения всех активных отзывов.
    Отображает список всех отзывов, которые имеют статус 'активный'.
    """
    model = Review
    extra_context = {
        'title': 'Все отзывы'
    }
    template_name = 'reviews/reviews.html'
    paginate_by = 2

    def get_queryset(self):
        """
        Возвращает только активные отзывы.
        Возвращает:
        QuerySet: Отзывы с активным статусом.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListview(ListView):
    """
    Представление для отображения неактивных отзывов.
    Отображает список всех отзывов, которые имеют статус 'неактивный'.
    """
    model = Review
    extra_context = {
        'title': 'Неактивные отзывы'
    }
    template_name = 'reviews/reviews.html'
    paginate_by = 2

    def get_queryset(self):
        """
        Возвращает только неактивные отзывы.
        Возвращает:
        QuerySet: Отзывы с неактивным статусом.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового отзыва.
    Позволяет авторизованным пользователям писать новые отзывы.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': 'Написать отзыв'
    }

    def form_valid(self, form):
        """
        Обрабатывает валидную форму и сохраняет новый отзыв.
        Проверяет, имеет ли пользователь право на создание отзыва.
        Генерирует слаг, если он временный.
        Параметры:
        form (ReviewForm): Валидная форма.
        Возвращает:
        HttpResponseRedirect: Перенаправление на страницу деталей отзыва.
        """
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden
        self.object = form.save()
        print(self.object.slug)
        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()
            print(self.object.slug)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ReviewDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей отзыва.
    Позволяет пользователям просматривать информацию о конкретном отзыве.
    """
    model = Review
    template_name = 'reviews/detail.html'
    extra_context = {
        'title': 'Просмотр отзыва'
    }


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования существующего отзыва.
    Позволяет авторизованным пользователям изменять свои отзывы.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': 'Изменить отзыв'
    }

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления.
        """
        return reverse('reviews:review_detail', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        """
        Получает объект отзыва для редактирования.
        Проверяет, является ли текущий пользователь автором отзыва или администратором.
        Параметры:
        queryset (QuerySet): Опциональный набор объектов.
        Возвращает:
        Объект отзыва.
        """
        self.object = super().get_object(queryset=queryset)
        if self.object.author != self.request.user and self.request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied()
        return self.object


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления отзыва.
    Позволяет пользователям с необходимыми правами удалять отзывы.
    """
    model = Review
    template_name = 'reviews/delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного удаления.
        """
        return reverse('reviews:reviews_list')


def review_toggle_activity(request, slug):
    """
    Переключает статус активности отзыва.
    Если отзыв активен, делает его неактивным, и наоборот.
    После изменения статуса перенаправляет пользователя на соответствующую страницу:
    - На страницу неактивных отзывов, если отзыв был активирован.
    - На страницу активных отзывов, если отзыв был деактивирован.
    Возвращает:
    Перенаправление на страницу списка отзывов в зависимости от нового статуса.
    """
    review_item = get_object_or_404(Review, slug=slug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False
        review_item.save()
        return redirect(reverse('reviews:reviews_deactivated'))
    else:
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:reviews_list'))
