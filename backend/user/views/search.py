from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.queries import *
import json

@csrf_exempt
def searchUsers(request):
    substr = json.loads(request.body)['substr']
    res = getUsersBySubstring(substr).batch()
    return JsonResponse({ 'users': list(res) })

@csrf_exempt
def getUser(request, key):
    userKey = json.loads(request.body)['key']
    res = getUser(userKey, targetKey=key).batch()[0]
    return JsonResponse(res)