from django.urls import path

from apps.home.views import *
urlpatterns = [
    # path('', home, name='home'),
    path('page/<str:page>', home, name='page'),
    path('process_all_images', process_all_images, name='process'),
]
