from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import json
import util

@csrf_exempt
def searchUsers(request):
    substr = json.loads(request.body)['substr']
    res = queries.getUsersBySubstring(substr).batch()
    return JsonResponse({'users': list(res)})


@csrf_exempt
def getUser(request, key):
    userKey = json.loads(request.body)['key']
    res = queries.getUserWithFriendship(userKey, targetKey=key).batch()[0]
    return JsonResponse(res)


@csrf_exempt
def getSummary(gameID):
    res = queries.getSummary(gameID).batch()[0]
    return JsonResponse(res)


@csrf_exempt
def getRating(request):
    data = json.loads(request.body)
    theme = data['theme']
    try:
        res = queries.getRating(theme).batch()[0]
    except:
        return util.returnError("Invalid theme.", 400)
    return JsonResponse({
        "rating": res['rating'],
        "numRatings": res['numRatings'],
    })