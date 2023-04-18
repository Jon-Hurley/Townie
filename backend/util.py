from django.http import JsonResponse
from hashlib import sha256
import jwt
import dotenv
import os
import time
dotenv.load_dotenv()

dt = 60 * 60

def returnError(errorMessage, errCode):
    return JsonResponse(
        {
            'errorMessage': errorMessage
        },
        status=errCode
    )

def getVerifyJWT(data):
    return jwt.encode(
        data,
        os.environ.get('REFRESH_TOKEN_SECRET'),
        algorithm="HS256"
    )

def getVerifyJWTData(token):
    return jwt.decode(
        token,
        os.environ.get('REFRESH_TOKEN_SECRET'),
        algorithms=["HS256"]
    )

def getUserFromTokenNoCheck(token):
    return jwt.decode(
        token,
        os.environ.get('JWT_TOKEN_SECRET'),
        algorithms=["HS256"]
    )

def getUserFromToken(token):
    user = getUserFromTokenNoCheck(token)
    t = time.time()

    # not past expiration time
    if user['expiration'] > t:
        return user, None
    
    # past expiration time by more than 30 minutes: log out
    if user['expiration'] < t + dt:
        return None, None
    
    # past expiration time by less than 30 minutes: refresh token
    user['expiration'] = t + dt
    newToken = jwt.encode(
        user,
        os.environ.get('JWT_TOKEN_SECRET'),
        algorithm="HS256"
    )
    
    return user, newToken
    
def returnUserPrivate(user):
    del user['_id']
    user['key'] = user['_key']
    del user['_key']
    del user['_rev']

    t = time.time()

    user['expiration'] = t + dt

    token = jwt.encode(
        user,
        os.environ.get('JWT_TOKEN_SECRET'),
        algorithm="HS256"
    )
    user['token'] = token

    del user['passwordHash']
    print("user is: ", user)
    return JsonResponse(user)

def returnUserPublic(user):
    del user['_id']
    del user['_rev']
    del user['passwordHash']
    user['key'] = user['_key']
    del user['_key']
    del user['login2FA']
    del user['hidingState']
    del user['phone']
    if 'stripeCustomerId' in user:
        del user['stripeCustomerId']
    if 'stripeSubscriptionId' in user:
        del user['stripeSubscriptionId']
    return JsonResponse(user)

def getPasswordHash(password, username):
    saltedPassword = f'{password}:{username}:hJ)R-PQ*CS'
    encodedPassword = saltedPassword.encode('utf-8')
    h = sha256()
    h.update(encodedPassword)
    hash = h.hexdigest()
    return hash