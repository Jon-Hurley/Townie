from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.queries import *
import twilio_con
import arango_con
import json

def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        phoneNumber = data.get('phoneNumber')

        res = getUsersBySubstring(username).batch()
        if len(list(res)) is 0:
            return JsonResponse({'success': False})
        createUser(username, password, phoneNumber)
        user = login(request, username=username, password=password)
        login(request, user)
    return JsonResponse({'success': True})

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = login(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

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