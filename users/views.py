import random
import string

from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_new_password, send_register_email


class UserRegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.
    Позволяет пользователям создавать новый аккаунт. После успешной регистрации
    отправляет электронное письмо с подтверждением.
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Регистрация пользователя',
        'message': 'Пожалуйста, заполните форму ниже, для успешной регистрации.'
    }

    def form_valid(self, form):
        """
        Обрабатывает валидную форму и сохраняет нового пользователя.
        Параметры:
        form (User RegisterForm): Валидная форма регистрации.
        Возвращает:
        Перенаправление на страницу входа после успешной регистрации.
        """
        self.object = form.save()
        send_register_email(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
    Представление для входа пользователя в систему.
    Позволяет пользователям вводить свои учетные данные для входа в аккаунт.
    """
    template_name = 'users/user_login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Вход в аккаунт',
        'message': 'Пожалуйста, заполните форму ниже, для успешного входа в аккаунт.'
    }


class UserProfileView(UpdateView):
    """
    Представление для отображения профиля пользователя.
    Позволяет пользователям просматривать информацию о своем профиле в режиме только для чтения.
    """
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'
    extra_context = {
        'title': 'Ваш профиль'
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    """
    Представление для обновления информации о пользователе.
    Позволяет пользователям изменять свои данные, такие как email, имя и аватар.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Обновить профиль',
        'message': 'Пожалуйста, заполните форму ниже, чтобы добавить, обновить данные.'
    }

    def get_object(self, queryset=None):
        """
        Получает текущего пользователя для обновления.
        Параметры:
        queryset: Опциональный набор объектов.
        Возвращает:
        User: Текущий пользователь.
        """
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    """
    Представление для изменения пароля пользователя.
    Позволяет пользователям изменять свой пароль с валидацией.
    """
    form_class = UserPasswordChangeForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Изменение пароля',
        'message': 'Пожалуйста, заполните форму ниже, для изменения пароля.'
    }


class UserLogoutView(LogoutView):
    """
    Представление для выхода пользователя из системы.
    Позволяет пользователям выходить из своего аккаунта.
    """
    template_name = 'users/user_logout.html'
    extra_context = {
        'title': 'Выход из аккаунта.'
    }


class UserListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка пользователей.
    Отображает всех активных пользователей в системе.
    """
    model = User
    extra_context = {
        'title': 'Питомник все наши пользователи'
    }
    template_name = 'users/users.html'
    paginate_by = 3

    def get_queryset(self):
        """
        Возвращает только активных пользователей.
        Возвращает:
        QuerySet: Активные пользователи.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class UserDetailView(DetailView):
    """
    Представление для отображения деталей профиля пользователя.
    Позволяет пользователям просматривать информацию о конкретном пользователе.
    """
    model = User
    template_name = 'users/user_detail_view.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительный контекст в шаблон.
        Параметры:
        **kwargs: Дополнительные параметры контекста.
        Возвращает:
        Объект контекста с добавленным заголовком профиля пользователя.
        """
        context_data = super().get_context_data()
        user_obj = self.get_object()
        context_data['title'] = f'Профиль пользователя {user_obj}'
        return context_data


@login_required
def user_generate_new_password_view(request):
    """
    Генерирует новый пароль для текущего пользователя и отправляет его на электронную почту.
    Новый пароль создается случайным образом и устанавливается для текущего пользователя.
    После этого отправляется электронное письмо с новым паролем.
    Параметры:
    request: Запрос от клиента.
    Возвращает:
    Перенаправление на главную страницу после успешного изменения пароля.
    """
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
