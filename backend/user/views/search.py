from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import json

@csrf_exempt
def searchUsers(request):
    substr = json.loads(request.body)['substr']
    res = queries.getUsersBySubstring(substr).batch()
    return JsonResponse({ 'users': list(res) })

@csrf_exempt
def getUser(request, key):
    if (request.method == 'POST'):
        print(key)
        res = queries.getUser(key).batch()[0]
        print(res)
        return JsonResponse(res)