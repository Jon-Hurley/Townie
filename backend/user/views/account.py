from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import twilio_con
import arango_con
import json
import requests
from hashlib import sha256

def hash(password):
    h = sha256()
    #password = str(password) + str(phoneNumber) + "Townie"
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
    print(username + ", " + password + ", " + str(phoneNumber))
    passwordHash = hash(password)

    try:
        arango_con.createUser(username, passwordHash, phoneNumber)
        print("made it past create user")
        res = arango_con.login(username, passwordHash) 
        data = res.batch()
        if len(data) == 0:
            return JsonResponse({'success': False})
        doc = data[0]
        print(doc)
        return JsonResponse(doc)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False})
    

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    print(request.body)
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    passwordHash = hash(password)
    print(username + ", " + passwordHash)
    res = arango_con.login(username, passwordHash) 
    data = res.batch()
    if len(data) == 0:
        return JsonResponse({'success': False})
    doc = data[0]
    print(doc)

    return JsonResponse(doc)


def loginWithToken(request):
    return JsonResponse({
        ":)": ":)"
    })

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def updateInfo(request, key):
    data = json.loads(request.body)
    username = data.get('username')
    phoneNumber = data.get('phoneNumber')
    res = arango_con.updateInfo(key, username, phoneNumber)
    data = res.batch()
    if len(data) == 0:
        return JsonResponse({'success': False})
    doc = data[0]
    print(doc)

    return JsonResponse(doc)

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def deleteUser(request):
    data = json.loads(request.body)
    key = data.get('key')
    try:
        res = arango_con.deleteUser(key)
    except:         
        return JsonResponse({'success': False})
    
    data = res.batch()
    print(len(data))
    if len(data) != 1:
        return JsonResponse({'success': False})
    return JsonResponse({ 'success': True })

def verification(request):
    data = json.loads(request.body)
    phoneNumber = data['phoneNumber']
    res = twilio_con.verifyUser(phoneNumber)
    return JsonResponse({ 'success': res })




def initiatePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })

def completePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })