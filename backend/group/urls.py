from django.urls import path
from . import views

urlpatterns = [
    path('create-game/', views.createGame),
    path('on-connect/', views.onConnect),
    path('on-disconnect/', views.onDisconnect),
    path('on-default/', views.onDefault),
    path('get-game/', views.getGame),
    path('get-destination/', views.getDestination),
]
