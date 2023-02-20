from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import arango_con
import json

@csrf_exempt
def searchUsers(request):
    substr = json.loads(request.body)['substr']
    res = arango_con.getUsersBySubstring(substr).batch()
    return JsonResponse({ 'users': list(res) })

@csrf_exempt
def getUser(request, key):
    userKey = json.loads(request.body)['key']
    res = arango_con.getUser(userKey, targetKey=key).batch()[0]
    return JsonResponse(res)