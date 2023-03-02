from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import twilio_con
import user.queries as queries
import json

def signup(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    phoneNumber = data.get('phoneNumber')

    res = queries.getUsersBySubstring(username).batch()
    if len(list(res)) is 0:
        return JsonResponse({'success': False})
    res2 = queries.createUser(username, password, phoneNumber)
    key = res2['_key']
    user = queries.login(request, username=username, password=password)
    login(request, user)
    return JsonResponse({'success': True})

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = queries.login(request, username=username, password=password)
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