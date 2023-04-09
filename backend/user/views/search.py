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
    res = queries.getUsersBySubstring(substr, userKey).batch()
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
        return util.returnError("Invalid theme.", 404)
    return JsonResponse({
        "rating": res['rating'],
        "numRatings": res['numRatings'],
    })


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
