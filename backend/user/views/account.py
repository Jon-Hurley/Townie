from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import twilio_con
import user.queries as queries
import json
import dotenv
import util
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
