from django.urls import path
from . import views

urlpatterns = [
    path('create-game/', views.createGame),
    path('on-connect/', views.onConnect),
    path('on-disconnect/', views.onDisconnect),
    path('on-default/', views.onDefault),
    path('get-game/', views.getGame),
    path('get-theme-list/', views.getThemeList),
    path('get-summary/', views.getSummary),
    # path('get-chat-password/', views.getChatPermissions),
]
