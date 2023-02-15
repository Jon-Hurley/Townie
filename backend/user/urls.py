from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('token-login/', views.loginWithToken),
    path('initiate-password-reset/', views.initiatePasswordReset),
    path('complete-password-reset/', views.completePasswordReset),
    path('request-friend/', views.requestFriend),
    path('accept-friend/', views.acceptFriend),
    path('remove-friend/', views.removeFriend)
]