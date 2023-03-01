from django.urls import path
from .views import friend, account, search

urlpatterns = [
    path('login/', account.login),
    path('signup/', account.signup),
    path('verification/', account.verification),
    path('token-login/', account.loginWithToken),
    path('account/', account.updateInfo),
    path('initiate-password-reset/', account.initiatePasswordReset),
    path('complete-password-reset/', account.completePasswordReset),
    path('delete/', account.deleteUser),
    
    path('search/', search.searchUsers),
    path('profile/<str:key>/', search.getUser),

    path('friends/', friend.getFriends),
    path('pending-friends/', friend.getPendingFriends),
    path('accept-friend/', friend.acceptFriend),
    path('reject-friend/', friend.rejectFriend),
    path('request-friend/', friend.requestFriend),
]