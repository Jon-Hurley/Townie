from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import json
import util
import twilio_con
import redis_con
import stripe_con

@csrf_exempt
def makePurchase(request):
    data = json.loads(request.body)
    purchasableKey = data['purchasableKey']

    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError("Invalid token.", 401)

    docs = queries.makePurchase(user['key'], purchasableKey).batch()
    if len(docs) == 0:
        return util.returnError("Unable to purchase item. Unknown error.", 404)
    if docs[0]['foundItem'] == False:
        return util.returnError("Unable to purchase item. Item not found.", 404)
    if docs[0]['hasPremiumReq'] == False:
        return util.returnError("Unable to purchase item. This item is only purchasable for premium users.", 401)
    if docs[0]['enoughPoints'] < 0:
        dp = -docs[0]['enoughPoints']
        return util.returnError(f'Unable to purchase item. You are {dp} points short.', 401)
    if docs[0]['alreadyPurchased'] == True:
        return util.returnError("Unable to purchase item. You have already purchased this item.", 404)

    userDocs = queries.getUserByUsername(user['username']).batch()
    if len(userDocs) == 0:
        return util.returnError("Unable to purchase item. Your account seems to have been terminated.", 404)

    return util.returnUserPrivate(userDocs[0])

@csrf_exempt
def activatePurchase(request):
    data = json.loads(request.body)
    purchasableKey = data['purchasableKey']

    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError("Invalid token.", 401)

    print(user['key'], purchasableKey)

    docs = queries.activatePurchase(user['key'], purchasableKey).batch()
    if len(docs) == 0:
        return util.returnError("Unable to activate purchase. You have not purchased this item.", 404)

    userDocs = queries.getUserByUsername(user['username']).batch()
    if len(userDocs) == 0:
        return util.returnError("Unable to activate item. Your account seems to have been terminated.", 404)

    return util.returnUserPrivate(userDocs[0])

@csrf_exempt
def getPurchasables(request):
    data = json.loads(request.body)

    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError("Invalid token.", 401)

    docs = queries.getPurchasables(user['key']).batch()
    
    return JsonResponse({
        'token': newToken,
        'purchasables': list(docs)
    })

@csrf_exempt
def initiateStripeSession(request):
    # Get user data from token
    data = json.loads(request.body)
    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)
    
    # Ensure user is not already premium
    if 'isPremium' in user and user['isPremium']:
        return util.returnError('Unable to upgrade to premium. You are already a premium user.', 401)
    
    # Check for existing session
    userKey = user['key']
    sessionId = redis_con.getUserSession(userKey)
    if sessionId is not None:
        print("Expiring session:", sessionId)
        stripe_con.expireSession(sessionId)
    
    # Create stripe session
    session = stripe_con.createCheckoutSession()
    redis_con.savePaymentSession(session.id, userKey)
    print("New Session:", session.id)

    return JsonResponse({
        'url': session.url,
        'token': newToken
    })

@csrf_exempt
def handleStripeWebhookEvent(request):
    eventData, eventType = stripe_con.getSubscriptionEvent(request)
    print("EVENT:", eventType)
    # CHECKOUT SESSION HANDLERS
    if eventType.startswith('checkout.session'):
        handleCheckoutSessionEvent(eventType, eventData)
    # SUBSCRIPTION HANDLERS
    elif eventType.startswith('customer.subscription'):
        handleSubscriptionEvent(eventType, eventData)
    return JsonResponse({})

def handleCheckoutSessionEvent(eventType, eventData):
    sessionId = eventData['id']
    customerId = eventData['customer']
    subscriptionId = eventData['subscription']

    # USER FINISHES CHECKOUT
    if eventType == 'checkout.session.completed':           
        userKey = redis_con.getSessionUser(sessionId)
        redis_con.deletePaymentSession(sessionId)

        user = queries.activatePremium(userKey, customerId, subscriptionId)['new']
        twilio_con.sendNotification(
            user['phone'],
            'Your Townie premium subscription has been activated. Thank you for your support!'
        )

def handleSubscriptionEvent(eventType, eventData):
    customerId = eventData['customer']
    subscriptionId = eventData['id']
    print(customerId, subscriptionId)

    # USER PAUSES SUBSCRIPTION
    if eventType == 'customer.subscription.paused':
        user = queries.updatePremium(customerId, False, subscriptionId).batch()[0]
        twilio_con.sendNotification(
            user['phone'],
            'Your Townie premium subscription has been paused. Please visit Townie to reactivate your subscription.'
        )
    # USER RESUMES SUBSCRIPTION
    elif eventType == 'customer.subscription.resumed':
        user = queries.updatePremium(customerId, True, subscriptionId).batch()[0]
        twilio_con.sendNotification(
            user['phone'],
            'Your Townie premium subscription has been resumed. Thank you for your support!'
        )
    # SUBSCRIPTION ENDS
    elif eventType == 'customer.subscription.deleted':
        users = queries.updatePremium(customerId, False, None).batch()
        if len(users) != 1:
            print("ERROR: Could not find user with customer id:", customerId)
            return
        user = users[0]
        twilio_con.sendNotification(
            user['phone'],
            'Your Townie premium subscription has been paused. Please visit Townie to reactivate your subscription.'
        )

@csrf_exempt
def cancelStripeSubscription(request):
    data = json.loads(request.body)
    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)

    if 'isPremium' not in user or not user['isPremium']:
        return util.returnError('You are not a premium user.', 401)

    if 'stripeCustomerId' not in user or not user['stripeCustomerId']:
        return util.returnError('Your stripe customer id seems to not exist.', 401)

    if 'stripeSubscriptionId' not in user or not user['stripeSubscriptionId']:
        return util.returnError('Your stripe subscription id seems to not exist.', 401)

    print("Canceling:", user['stripeCustomerId'])
    stripe_con.cancelSubscription(user['stripeSubscriptionId'])
    user = queries.updatePremium(user['key'], False).batch()[0]

    twilio_con.sendNotification(
        user['phone'],
        'Your Townie premium subscription has been canceled. At the end of the billing cycle, you will no longer have access to Townie Premium features.'
    )

    return JsonResponse({
        'token': newToken
    })