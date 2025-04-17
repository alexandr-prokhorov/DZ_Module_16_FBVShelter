from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from dogs.models import Breed, Dog
from dogs.forms import DogForm

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

class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Добавить собаку',
        'message': 'Пожалуйста, заполните форму ниже, чтобы добавить новую собаку.'
    }
    success_url = reverse_lazy('dogs:dogs_list')

class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'
    extra_context = {
        'title': 'Подробная информация'
    }

# @login_required
# def dog_detail_view(request, pk):
#     dog_object = Dog.objects.get(pk=pk)
#     context = {
#         'object': dog_object,
#         'title': f'ВЫ выбрали: {dog_object.name}. Порода: {dog_object.breed.name}.'
#     }
#     return render(request, 'dogs/detail.html', context)

@login_required
def dog_update_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:dog_detail', args={pk: pk}))
    context = {
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    }
    return render(request, "dogs/create_update.html", context)

@login_required
def dog_delete_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return  HttpResponseRedirect(reverse('dogs:dogs_list'))
    context = {
        'object': dog_object,
    }
    return render(request, 'dogs/delete.html', context)