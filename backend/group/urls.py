from django.urls import path
from . import views

urlpatterns = [
    #I ADDED THIS
    path('map', views.map, name='map'),
]