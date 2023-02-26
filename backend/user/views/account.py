from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import twilio_con
import arango_con
import json
from hashlib import sha256

def hash(password, phoneNumber):
    h = sha256()
    password += phoneNumber + "Townie"
    temp = password.encode('utf-8')
    h.update(temp)
    hash = h.hexdigest()
    return hash

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def signup(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    phoneNumber = data.get('phoneNumber')

    passwordHash = hash(password, phoneNumber)

    try:
        user = arango_con.createUser(username, passwordHash, phoneNumber)
        return login(JsonResponse({'username': username, 'password': password, 'phoneNumber' : phoneNumber}))
    except:
        return JsonResponse({'success': False})
    

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    phoneNumber = data.get('phoneNumber')
    passwordHash = hash(password, phoneNumber)
    res = arango_con.login(request, username, passwordHash)
    data = json.loads(res.body)
    if not data.get('success'):
        return JsonResponse({'success': False})
    key = data.get('key')
    return JsonResponse({ 'success': True,
                          'key': key, 
                          'username' : username,
                          'phoneNumber': data['phone'],
                          'points': data['points'],
                          'rank': data['ranks'],
                          'purchases': data['purchases']})

def loginWithToken(request):
    return JsonResponse({
        ":)": ":)"
    })

def updateInfo(request):
    data = json.loads(request.body)
    username = data.get('username')
    key = data.get('key')
    phoneNumber = data.get('phoneNumber')
    res = arango_con.updateInfo(key, username, phoneNumber)
    data = json.loads(res.body)
    if not data.get('success'):
        return JsonResponse({'success': False})
    return JsonResponse({ 'success': True,
                          'key': key, 
                          'username' : username,
                          'phoneNumber': data['phone'],
                          'points': data['points'],
                          'rank': data['ranks'],
                          'purchases': data['purchases']})

def deleteUser(request):
    data = json.loads(request.body)
    key = data.get('key')
    res = arango_con.deleteUser(key)
    data = json.loads(res.body)
    if not data.get('success'):
        return JsonResponse({'success': False})
    return JsonResponse({ 'success': True })

def verification(request): 
    data = json.loads(request.body)



def initiatePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })

def completePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })