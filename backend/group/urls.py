from django.urls import path
from . import views
from . import scraper

urlpatterns = [
    path('create-game/', views.createGame),
    path('on-connect/', views.onConnect),
    path('scraper/', scraper.map)
]