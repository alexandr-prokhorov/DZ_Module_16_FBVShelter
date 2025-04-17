import random
import string

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import  LoginView, PasswordChangeView, LogoutView
from django.views.generic import  CreateView, UpdateView
from django.urls import reverse_lazy

from users.models import  User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_new_password, send_register_email

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Регистрация пользователя',
        'message': 'Пожалуйста, заполните форму ниже, для успешной регистрации.'
    }


class UserLoginView(LoginView):
    template_name = 'users/user_login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Вход в аккаунт',
        'message': 'Пожалуйста, заполните форму ниже, для успешного входа в аккаунт.'
    }

class UserProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'
    extra_context = {
        'title': 'Ваш профиль'
    }

    def get_object(self, queryset=None):
        return self.request.user

class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Обновить профиль',
        'message': 'Пожалуйста, заполните форму ниже, чтобы добавить, обновить данные.'
    }

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Изменение пароля',
        'message': 'Пожалуйста, заполните форму ниже, для изменения пароля.'
    }

class UserLogoutView(LogoutView):
    template_name = 'users/user_logout.html'
    extra_context = {
        'title': 'Выход из аккаунта.'
    }

# def user_logout_view(request):
#     logout(request)
#     return redirect('dogs:index')

@login_required
def user_generate_new_password_view(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))