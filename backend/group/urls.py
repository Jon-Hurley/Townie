from django.urls import path
from . import views

urlpatterns = [
    path('create-game/', views.createGame),
    path('on-connect/', views.onConnect)
]