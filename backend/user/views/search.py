from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import json
import util


@csrf_exempt
def searchUsers(request):
    body = json.loads(request.body)
    substr = body['substr']
    userKey = body['key']
    if len(substr) != 0:
        res = queries.getUsersBySubstring(substr, userKey).batch()
    else:
        res = queries.getOnlySuggestedUsers(userKey).batch()
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
def getGameLog(request):
    userKey = json.loads(request.body)['key']
    res = queries.getGameLog(userKey).batch()
    print(res)
    return JsonResponse({'games': list(res)})


@csrf_exempt
def submitRating(request):
    data = json.loads(request.body)
    theme = data['theme']
    rating = data['rating']
    numRatings = data['numRatings']
    try:
        queries.submitRating(theme, rating, numRatings)
    except:
        return util.returnError("Invalid theme or rating.", 400)
    return JsonResponse({})
