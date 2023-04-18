from django.http import JsonResponse
from hashlib import sha256
import jwt
import dotenv
import os
import time
dotenv.load_dotenv()


# TOKEN EXPIRATION TIME
dt = 60 * 60


def returnError(errorMessage, errCode):
    return JsonResponse(
        {
            'errorMessage': errorMessage
        },
        status=errCode
    )

def returnUserPrivate(user):
    del user['_id']
    del user['_rev']
    user['key'] = user['_key']
    del user['_key']
    purchases = user['purchases']
    del user['purchases'] # remove purchases info from token

    t = time.time()
    user['expiration'] = t + dt

    token = _encodeUserJWT(user)
    user['token'] = token
    user['purchases'] = purchases # restore purchases info

    del user['passwordHash']
    return JsonResponse(user)

def returnUserPublic(user):
    del user['_id']
    del user['_rev']
    del user['passwordHash']
    del user['login2FA']
    del user['hidingState']
    del user['phone']
    user['key'] = user['_key']
    del user['_key']

    if 'stripeCustomerId' in user:
        del user['stripeCustomerId']
    if 'stripeSubscriptionId' in user:
        del user['stripeSubscriptionId']
    
    return JsonResponse(user)


def encodeVerifyJWT(data):
    return jwt.encode(
        data,
        os.environ.get('REFRESH_TOKEN_SECRET'),
        algorithm="HS256"
    )

def decodeVerifyJWT(token):
    return jwt.decode(
        token,
        os.environ.get('REFRESH_TOKEN_SECRET'),
        algorithms=["HS256"]
    )

def _decodeUserJWT(token):
    return jwt.decode(
        token,
        os.environ.get('JWT_TOKEN_SECRET'),
        algorithms=["HS256"]
    )

def _encodeUserJWT(user):
    return jwt.encode(
        user,
        os.environ.get('JWT_TOKEN_SECRET'),
        algorithm="HS256"
    )

def decodeUserJWT(token):
    user = _decodeUserJWT(token)
    t = time.time()

    # not past expiration time
    if user['expiration'] > t:
        return user, None
    
    # past expiration time by more than 60 minutes: log out
    if user['expiration'] < t + dt:
        return None, None
    
    # past expiration time by less than 60 minutes: refresh token
    user['expiration'] = t + dt
    newToken = jwt.encode(
        user,
        os.environ.get('JWT_TOKEN_SECRET'),
        algorithm="HS256"
    )
    
    return user, newToken


def getPasswordHash(password, username):
    saltedPassword = f'{password}:{username}:hJ)R-PQ*CS'
    encodedPassword = saltedPassword.encode('utf-8')
    h = sha256()
    h.update(encodedPassword)
    hash = h.hexdigest()
    return hash