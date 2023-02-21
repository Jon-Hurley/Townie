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
    if data.get('success') == False:
        return JsonResponse({'success': False})
    key = data.get('key')
    return JsonResponse({'success': True,
                          'key': key, 
                          'username' : username})

def loginWithToken(request):
    return JsonResponse({
        ":)": ":)"
    })


def initiatePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })

def completePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })