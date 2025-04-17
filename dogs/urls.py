from django.urls import path
from dogs.views import (index, breeds_list_view, breed_dogs_list_view, DogListView, dog_create_view, dog_detail_view,
                        dog_update_view, dog_delete_view)
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('breeds/', breeds_list_view, name='breeds'),
    path('breeds/<int:pk>/dogs/', breed_dogs_list_view, name='breed_dogs'),

    path('dogs/', DogListView.as_view(), name='dogs_list'),
    path('dogs/create/', dog_create_view, name='dog_create'),
    path('dogs/detail/<int:pk>/', dog_detail_view, name='dog_detail'),
    path('dogs/update/<int:pk>/', dog_update_view, name='dog_update'),
    path('dogs/delete/<int:pk>/', dog_delete_view, name='dog_delete'),
]