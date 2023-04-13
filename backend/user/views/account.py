from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import twilio_con
import user.queries as queries
import json
import dotenv
import util
import stripe_con
import redis_con
dotenv.load_dotenv()

@csrf_exempt  # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def signup(request):
    print("Running")
    data = json.loads(request.body)
    print(data)
    phone = data['phone']
    username = data['username']

    try:
        docs = queries.getUserFromPhoneOrUsername(phone, username).batch()
    except Exception as e:
        print("error in first try")
        return util.returnError(e.error_message, e.http_code)

    if len(docs) != 0:
        return util.returnError('There already exists an account with this phone number or username.', 401)

    res = twilio_con.sendVerification(phone)
    print(res)
    return JsonResponse({})


@csrf_exempt
def verifySignup(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    phone = data['phone']
    otp = data['otp']

    if password.find(':') != -1:
        return util.returnError("Passwords may not contain colons.", 400)

    res = twilio_con.testVerification(phone, otp)
    if not res:
        return util.returnError('Invalid OTP.', 401)

    # ADD ANY OTHER PASSWORD RESTRICTIONS

    passwordHash = util.getPasswordHash(password, username)

    try:
        doc = queries.createUser(username, passwordHash, phone)
    except Exception as e:
        em = e.error_message
        if em.find('unique constraint violated') != -1:
            return util.returnError('This username or phone number is already taken.', e.http_code)
        return util.returnError(em, e.http_code)

    return util.returnUserPrivate(doc['new'])


@csrf_exempt  # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']

    if password.find(':') != -1:
        return util.returnError("Passwords may not contain colons.", 400)

    try:
        docs = queries.getUserByUsername(username).batch()
    except Exception as e:
        return util.returnError(e.error_message, e.http_code)
    
    if len(docs) == 0:
        return util.returnError('Invalid username.', 401)

    user = docs[0]
    passwordHash = util.getPasswordHash(password, username)
    if user['passwordHash'] != passwordHash:
        return util.returnError('Invalid password.', 401)

    if user['login2FA']:
        res = twilio_con.sendVerification(user['phone'])
        return JsonResponse({
            'verifyToken': util.getVerifyJWT(user)
        })
    
    return util.returnUserPrivate(user)

@csrf_exempt
def verifyLogin(request):
    data = json.loads(request.body)
    otp = data['otp']

    verifyToken = data['verifyToken']
    user = util.getVerifyJWTData(verifyToken)
    phone = user['phone']

    res = twilio_con.testVerification(phone, otp)
    if not res:
        return util.returnError('Invalid OTP.', 401)
    
    return util.returnUserPrivate(user)

@csrf_exempt
def loginWithToken(request):
    data = json.loads(request.body)

    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)

    username = user['username']
    try:
        docs = queries.getUserByUsername(username).batch()
    except Exception as e:
        return util.returnError(e.error_message, e.http_code)

    if len(docs) == 0:
        return util.returnError('Invalid username.', 401)

    return util.returnUserPrivate(docs[0])


@csrf_exempt
def updateInfo(request):
    data = json.loads(request.body)
    enteredPassword = data['password']
    newUsername = data['newUsername']
    newLogin2FA = data['newLogin2FA']
    newPhone = data['newPhone']
    newHidingState = data['newHidingState']
    
    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)
    key = user['key']
    passwordHash = user['passwordHash']
    oldUsername = user['username']

    expectedInputHash = util.getPasswordHash(enteredPassword, oldUsername)
    if expectedInputHash != passwordHash:
        return util.returnError('Incorrect password entered.', 400)

    newPasswordHash = passwordHash if newUsername == oldUsername\
                      else util.getPasswordHash(enteredPassword, newUsername)
    
    try:
        docs = queries.updateInfo(
            key, newUsername, newPhone, newPasswordHash, newLogin2FA,
            newHidingState
        ).batch()
    except Exception as e:
        em = e.error_message
        if em.find('unique constraint violated') != -1:
            return util.returnError('This username or phone number is already taken.', e.http_code)
        return util.returnError(em, e.http_code)

    if len(docs) == 0:
        # NOTE: could also be invalid key, but I trust not
        return util.returnError('Invalid password.', 401)

    return util.returnUserPrivate(docs[0])


@csrf_exempt
def updatePlayableTime(request):
    data = json.loads(request.body)
    key = data['key']
    weeklyGamePlayed = data['weeklyGamePlayed']
    newTime = data['newTime']

    docs = queries.UpdatePlayableInfo(key, weeklyGamePlayed, newTime).batch()
    return util.returnUserPrivate(docs[0])

@csrf_exempt
def deleteUser(request):
    data = json.loads(request.body)

    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)

    try:
        docs = queries.deleteUser(user['key'], user['passwordHash']).batch()
    except Exception as e:
        print(e.error_message, e.http_code)
        return util.returnError(e.error_message, e.http_code)

    if len(docs) == 0:
        return util.returnError('Unauthorized.', 401)  # invalid passwordHash or key

    return JsonResponse({
        "token": newToken
    })

@csrf_exempt
def initiatePasswordReset(request):
    data = json.loads(request.body)
    phone = data['phone']

    try:
        docs = queries.getUserFromPhone(phone).batch()
    except Exception as e:
        return util.returnError(e.error_message, e.http_code)

    if len(docs) != 1:
        return util.returnError('Invalid phone.', 401)

    res = twilio_con.sendVerification(phone)
    print(res)

    return JsonResponse({})


@csrf_exempt
def completePasswordReset(request):
    data = json.loads(request.body)
    phone = data['phone']
    otp = data['otp']
    newPassword = data['newPassword']

    res = twilio_con.testVerification(phone, otp)
    if not res:
        return util.returnError('Invalid OTP.', 401)

    try:
        docs = queries.getUserFromPhone(phone).batch()
    except Exception as e:
        return util.returnError(e.error_message, e.http_code)

    if len(docs) != 1:
        return util.returnError('Invalid phone.', 401)

    user = docs[0]
    passwordHash = user['passwordHash']
    username = user['username']
    userKey = user['_key']

    newPasswordHash = util.getPasswordHash(newPassword, username)
    if newPasswordHash != passwordHash:
        try:
            doc = queries.updatePassword(userKey, newPasswordHash)
        except Exception as e:
            return util.returnError("Invalid user key.", 500)

    return JsonResponse({})

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