from django.shortcuts import render
from django.template.context_processors import request

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.http import Http404
from django.forms import inlineformset_factory

from dogs.models import Breed, Dog, DogParent
from dogs.forms import DogForm, DogParentForm

def index(request):
    context = {
        'objects_list': Breed.objects.all()[:6],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)

def breeds_list_view(request):
    context = {
        'objects_list': Breed.objects.all(),
        'title': 'Питомник - Все наши породы'
    }
    return render(request, 'dogs/breeds.html', context)

def breed_dogs_list_view(request, pk: int):
    breed_item = Breed.objects.get(pk=pk)
    # breed_item = get_object_or_404(Breed, pk=pk)
    context = {
        'objects_list': Dog.objects.filter(breed_id=pk),
        'title': f'Собаки породы - {breed_item.name}',
        'breed_pk': breed_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)

class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'

class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Добавить собаку',
        'message': 'Пожалуйста, заполните форму ниже, чтобы добавить новую собаку.'
    }
    success_url = reverse_lazy('dogs:dogs_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Подробная информация о {self.object.name}'
        return context_data

class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Изменить информацию о собаке',
        'message': 'Пожалуйста, заполните форму ниже, чтобы добавить новую информацию о собаке.'
    }

    def get_success_url(self):
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return  self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(Dog, DogParent, form=DogParentForm, extra=1)
        if self.request.method == 'POST':
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    extra_context = {
        'title': 'Удалить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')

