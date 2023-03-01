from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import twilio_con
import user.queries as queries
import json
from hashlib import sha256
from arango import DocumentInsertError

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
    return JsonResponse(user)

def returnUserPublic(user):
    del user['_id']
    del user['_rev']
    del user['passwordHash']
    user['key'] = user['_key']
    del user['_key']
    return JsonResponse(user)

def getPasswordHash(password, username):
    saltedPassword = f'{password}:{username}:hJ)R-PQ*CS'
    encodedPassword = saltedPassword.encode('utf-8')
    h = sha256()
    h.update(encodedPassword)
    hash = h.hexdigest()
    return hash

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def signup(request):
    data = json.loads(request.body)
    username = data['username']
    phone = data['phone']
    password = data['password']

    if password.find(':') != -1:
        return returnError("Passwords must not contain colons.", 400)
    # ADD ANY OTHER PASSWORD RESTRICTIONS

    passwordHash = getPasswordHash(password, username)
    
    try:
        doc = queries.createUser(username, passwordHash, phone)
    except Exception as e:
        em = e.error_message
        if em.find('unique constraint violated') != -1:
            return returnError('This username is already taken.', e.http_code)
        return returnError(em, e.http_code)

    return returnUserPrivate(doc['new'])

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']

    try:
        docs = queries.getUserByUsername(username).batch()
    except Exception as e:
        return returnError(e.error_message, e.http_code)
    
    if len(docs) == 0:
        return returnError('Invalid username.', 401)
    
    user = docs[0]
    passwordHash = getPasswordHash(password, username)
    if user['passwordHash'] != passwordHash:
        return returnError('Invalid password.', 401)

    return returnUserPrivate(user)

@csrf_exempt
def updateInfo(request):
    data = json.loads(request.body)
    key = data['key']
    username = data['username']
    password = data['password']
    passwordHash = data['passwordHash']
    
    newUsername = data['newUsername']
    newPhone = data['newPhone']

    newPasswordHash = passwordHash
    if newUsername != username:
        newPasswordHash = getPasswordHash(password, newUsername)
    
    try:
        docs = queries.updateInfo(
            key, passwordHash,
            newUsername, newPhone, newPasswordHash
        ).batch()
    except Exception as e:
        em = e.error_message
        if em.find('unique constraint violated') != -1:
            return returnError('This username is already taken.', e.http_code)
        return returnError(em, e.http_code)
    
    if len(docs) == 0:
        return returnError('Invalid password.', 401) # NOTE: could also be invalid key, but I trust not

    return returnUserPrivate(docs[0])

@csrf_exempt
def deleteUser(request):
    data = json.loads(request.body)
    key = data['key']
    passwordHash = data['passwordHash']

    try:
        docs = queries.deleteUser(key, passwordHash).batch()
    except Exception as e:
        return returnError(e.error_message, e.http_code)

    if len(docs) == 0:
        return returnError('Unauthorized.', 401) # invalid passwordHash or key

    return JsonResponse({})

# TO-DO:

def loginWithToken(request):
    return JsonResponse({
        ":)": ":)"
    })

def verification(request):
    data = json.loads(request.body)
    phone = data['phone']
    res = twilio_con.verifyUser(phone)
    return JsonResponse({})

def initiatePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })

def completePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })