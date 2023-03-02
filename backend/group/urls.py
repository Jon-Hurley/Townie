from django.urls import path
from . import views, scraper

urlpatterns = [
    path('create-game/', views.createGame),
    path('on-connect/', views.onConnect),
    path('on-disconnect/', views.onDisconnect),
    path('on-default/', views.onDefault),
    path('map', scraper.map)
]