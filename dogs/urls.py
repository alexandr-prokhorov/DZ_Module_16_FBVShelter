from django.urls import path
from dogs.views import index, breeds_list_view, breed_dogs_list_view, dogs_list_view, dog_create_view
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('breeds/', breeds_list_view, name='breeds'),
    path('breeds/<int:pk>/dogs/', breed_dogs_list_view, name='breed_dogs'),

    path('dogs/', dogs_list_view, name='dogs_list'),
    path('dogs/create/', dog_create_view, name='dog_create'),
]