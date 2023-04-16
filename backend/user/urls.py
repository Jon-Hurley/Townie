from django.urls import path
from .views import friend, account, search, store

urlpatterns = [
    path('login/', account.login),
    path('verify-login/', account.verifyLogin),
    path('signup/', account.signup),
    path('verify-signup/', account.verifySignup),

    path('token-login/', account.loginWithToken),
    path('initiate-password-reset/', account.initiatePasswordReset),
    path('complete-password-reset/', account.completePasswordReset),
    path('update/', account.updateInfo),
    path('delete/', account.deleteUser),

    path('search/', search.searchUsers),
    path('profile/<str:key>/', search.getUser),
    path('rating/', search.getRating),
    path('gameLog/', search.getGameLog),

    path('friends/', friend.getFriends),
    path('pending-friends/', friend.getPendingFriends),
    path('accept-friend/', friend.acceptFriend),
    path('reject-friend/', friend.rejectFriend),
    path('request-friend/', friend.requestFriend),

    path('updateTime/', account.updatePlayableTime),
    path('submit-rating/', search.submitRating),

    path('stripe-web-hook/', store.handleStripeWebhookEvent),
    path('initiate-subscription/', store.initiateStripeSession),
    path('cancel-subscription/', store.cancelStripeSubscription),

    path('purchase/', store.makePurchase),
    path('purchasables/', store.getPurchasables),
    path('activate-purchase/', store.activatePurchase),
]