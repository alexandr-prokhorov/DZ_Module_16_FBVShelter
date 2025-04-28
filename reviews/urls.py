from django.urls import path

from reviews.apps import ReviewsConfig

from reviews.views import ReviewListview, ReviewDeactivatedListview


app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListview.as_view(), name='reviews_list'),
    path('deactivated', ReviewDeactivatedListview.as_view(), name='reviews_deactivated')
]