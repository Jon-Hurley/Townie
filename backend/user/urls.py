from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('token-login/', views.loginWithToken),
    path('initiate-password-reset/', views.initiatePasswordReset),
    path('complete-password-reset/', views.completePasswordReset),
    
    path('search-users/', views.searchUsers),

    path('friends/', views.getFriends),
    path('pending-friends/', views.getPendingFriends),
    path('accept-friend/', views.acceptFriend),
    path('reject-friend/', views.rejectFriend),

    # path('request-friend/', views.requestFriend),
]