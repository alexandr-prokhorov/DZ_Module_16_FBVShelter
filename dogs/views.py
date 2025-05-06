from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from dogs.models import Breed, Dog, DogParent
from dogs.forms import DogForm, DogParentForm, DogAdminForm
from dogs.services import send_views_mail
from users.models import UserRoles


class IndexView(LoginRequiredMixin, ListView):
    """
    Представление главной страницы питомника.
    Отображает список всех пород собак с пагинацией.
    """
    model = Breed
    template_name = 'dogs/index.html'
    extra_context = {
        'title': 'Питомник - Главная'
    }

    paginate_by = 3

    def get_queryset(self):
        """
        Возвращает все породы собак.
        Возвращает:
        QuerySet: Все объекты породы.
        """
        return Breed.objects.all()


class BreedsListView(LoginRequiredMixin, ListView):
    """
    Представление списка всех пород собак.
    Отображает все породы с пагинацией.
    """
    model = Breed
    template_name = 'dogs/breeds.html'

    extra_context = {
        'title': "Все наши породы"
    }
    paginate_by = 3


class DogBreedSearchListView(LoginRequiredMixin, ListView):
    """
    Представление результатов поиска пород собак.
    Отображает породы, соответствующие поисковому запросу.
    """
    model = Breed
    template_name = 'dogs/breeds.html'
    extra_context = {
        'title': 'Результаты поискового запроса'
    }

    def get_queryset(self):
        """
        Возвращает породы, соответствующие поисковому запросу.
        Возвращает:
        QuerySet: Породы, соответствующие запросу.
        """
        query = self.request.GET.get('q')
        print(query)
        object_list = Breed.objects.filter(
            Q(name__icontains=query),
        )
        return object_list


class DogBreedListView(LoginRequiredMixin, ListView):
    """
    Представление списка собак выбранной породы.
    Отображает собак, относящихся к определенной породе.
    """
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Собаки выбранной породы'
    }
    paginate_by = 3

    def get_queryset(self):
        """
        Возвращает собак, относящихся к выбранной породе.
        Возвращает:
        QuerySet: Собаки выбранной породы.
        """
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get('pk'))
        return queryset


class DogListView(ListView):
    """
    Представление списка всех активных собак.
    Отображает только активных собак с пагинацией.
    """
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'
    paginate_by = 3

    def get_queryset(self):
        """
        Возвращает только активных собак.
        Возвращает:
        QuerySet: Активные собаки.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivatedListView(LoginRequiredMixin, ListView):
    """
    Представление списка неактивных собак.
    Отображает неактивных собак в зависимости от роли пользователя.
    """
    model = Dog
    extra_context = {
        'title': "Питомник - неактивные собаки"
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """
        Возвращает неактивных собак в зависимости от роли пользователя.
        Возвращает:
        QuerySet: Неактивные собаки.
        """
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    """
    Представление результатов поиска собак.
    Отображает собак, соответствующих поисковому запросу.
    """
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Результаты поискового запроса'
    }

    def get_queryset(self):
        """
        Возвращает собак, соответствующих поисковому запросу.
        Возвращает:
        QuerySet: Собаки, соответствующие запросу.
        """
        query = self.request.GET.get('q')
        print(query)
        object_list = Dog.objects.filter(
            Q(name__icontains=query), is_active=True,
        )
        return object_list


class DogCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой собаки.
    Отображает форму для добавления новой собаки и сохраняет её в базе данных.
    Доступно только для пользователей с ролью USER.
    """
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Добавить собаку',
        'message': 'Пожалуйста, заполните форму ниже, чтобы добавить новую собаку.'
    }
    success_url = reverse_lazy('dogs:dogs_list')

    def form_valid(self, form):
        """
        Обрабатывает валидную форму.
        Устанавливает владельца собаки и сохраняет объект.
        Если пользователь не имеет права добавлять собаку, выбрасывает PermissionDenied.
        Параметры:
        form (DogForm): Валидная форма.
        Возвращает:
        HttpResponseRedirect: Перенаправление на страницу списка собак.
        """
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    """
    Представление для отображения подробной информации о собаке.
    Отображает информацию о выбранной собаке и увеличивает количество просмотров.
    Если количество просмотров кратно 20, отправляет уведомление владельцу.
    """
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительный контекст в шаблон.
        Параметры:
        **kwargs: Дополнительные параметры.
        """
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Подробная информация о {object_}'
        dog_object_increase = get_object_or_404(Dog, pk=object_.pk)
        if object_.owner != self.request.user:
            dog_object_increase.views_count()
        if object_.owner:
            object_owner_email = object_.owner.email
            if dog_object_increase.views % 20 == 0 and dog_object_increase.views != 0:
                send_views_mail(dog_object_increase.name, object_owner_email, dog_object_increase.views)
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования информации о собаке.
    Позволяет владельцу или администратору изменять информацию о собаке.
    """
    model = Dog
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Изменить информацию о собаке',
        'message': 'Пожалуйста, заполните форму ниже, чтобы добавить новую информацию о собаке.'
    }

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления.
        """
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """
        Получает объект собаки для редактирования.
        Проверяет, является ли текущий пользователь владельцем собаки или администратором.
        Если нет, выбрасывает PermissionDenied.
        Параметры:
        queryset (QuerySet): Опциональный набор объектов.
        Возвращает:
        Объект собаки.
        """
        self.object = super().get_object(queryset)
        # if self.object.owner != self.request.user and not self.request.user.is_staff:
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object

    def get_form_class(self):
        """
        Возвращает класс формы в зависимости от роли пользователя.
        Возвращает:
        Класс формы для редактирования собаки.
        """
        dog_forms = {
            'admin': DogAdminForm,
            'moderator': DogForm,
            'user': DogForm,
        }
        user_role = self.request.user.role
        dog_form_class = dog_forms[user_role]
        return dog_form_class

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительный контекст в шаблон.
        Параметры:
        **kwargs: Дополнительные параметры.
        """
        context_data = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(Dog, DogParent, form=DogParentForm, extra=1)
        if self.request.method == 'POST':
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        """
        Обрабатывает валидную форму и сохраняет данные.
        Сохраняет объект собаки и связанные данные о родителях, если форма валидна.
        """
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления собаки.
    Позволяет пользователю с необходимыми правами удалить собаку из базы данных.
    """
    model = Dog
    template_name = 'dogs/delete.html'
    extra_context = {
        'title': 'Удалить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')
    permission_required = 'dogs.delete_dog'
    permission_denied_message = "У вас нет нужных прав для этого действия"


def dog_toggle_activity(request, pk):
    """
    Переключает активность собаки.
    Если собака активна, делает её неактивной, и наоборот.
    Перенаправляет на страницу списка собак после изменения.
    Параметры:
    request : Запрос от клиента.
    pk : Первичный ключ собаки.
    Возвращает:
    Перенаправление на страницу списка собак.
    """
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect((reverse('dogs:dogs_list')))
