import json
import arango_con
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .twilio_con import t

def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        phoneNumber = data.get('phoneNumber')

        res = arango_con.getUsersBySubstring(username).batch()
        if len(list(res)) is 0:
            return JsonResponse({'success': False})
        arango_con.createUser(username, password, phoneNumber)
        user = arango_con.login(request, username=username, password=password)
        login(request, user)
    return JsonResponse({'success': True})

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = arango_con.login(request, username=username, password=password)
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


def requestFriend(request):
    return JsonResponse({
        'status': 'failed!'
    })

def acceptFriend(request):
    return JsonResponse({
        'newFriendsList': []
    })

def removeFriend(request):
    return JsonResponse({
        'newFriendsList': []
    })