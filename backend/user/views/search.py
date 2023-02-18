from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import arango_con
import json

@csrf_exempt
def searchUsers(request):
    res = arango_con.getUsersBySubstring(
        json.loads(request.body)['substr']
    ).batch()
    return JsonResponse({ 'users': list(res) })
