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
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm
from users.services import send_new_password, send_register_email

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }


class UserLoginView(LoginView):
    template_name = 'users/user_login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Вход в аккаунт'
    }


@login_required
def user_profile_view(request):
    user_object = request.user
    # if user_object.first_name:
    #     user_name = user_object.first_name + ' ' + user_object.last_name
    # else:
    #     user_name = "Anonymous"

    # context = {
    #     'title': f'Ваш профиль {user_name}'
    # }
    #
    context = {
        'title': f'Ваш профиль {user_object.first_name} {user_object.last_name}'
    }
    return render(request, 'users/user_profile_read_only.html', context)

@login_required
def user_update_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('users:user_profile'))
    else:
        form = UserUpdateForm(instance=user_object)

        context = {
            'object': user_object,
            'title': f'Изменить профиль {user_object.first_name} {user_object.last_name}',
            'form': form
        }
        return render(request, 'users/user_update.html', context)

@login_required
def user_change_password_view(request):
    user_object = request.user
    form = UserPasswordChangeForm(user_object, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, 'Пароль был успешно изменен!')
            return HttpResponseRedirect(reverse('users:user_profile'))
        messages.error(request, 'Не удалось изменить пароль')
    context = {
        'form': form
    }
    return render(request, 'users/user_change_password.html', context)

def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')

@login_required
def user_generate_new_password_view(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))