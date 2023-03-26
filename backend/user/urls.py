from django.urls import path
from .views import friend, account, search

urlpatterns = [
    path('login/', account.login),
    path('signup/', account.signup),
    path('verify-signup/', account.verifySignup),
    
    path('token-login/', account.loginWithToken),
    path('initiate-password-reset/', account.initiatePasswordReset),
    path('complete-password-reset/', account.completePasswordReset),
    path('update/', account.updateInfo),
    path('delete/', account.deleteUser),

    path('search/', search.searchUsers),
    path('profile/<str:key>/', search.getUser),
    path('gameLog/', search.getGameLog),

    path('friends/', friend.getFriends),
    path('pending-friends/', friend.getPendingFriends),
    path('accept-friend/', friend.acceptFriend),
    path('reject-friend/', friend.rejectFriend),
    path('request-friend/', friend.requestFriend),
]