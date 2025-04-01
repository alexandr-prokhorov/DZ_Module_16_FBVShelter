from django.urls import path
from dogs.views import index, breeds_list, breed_dogs_list
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('breeds/', breeds_list, name='breeds'),
    path('breeds/<int:pk>/dogs/', breed_dogs_list, name='breed_dogs')
]