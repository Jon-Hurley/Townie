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
def getGameLog(request):
    body = json.loads(request.body)
    targetKey = body['key']
    res = queries.getGameLog(targetKey).batch()
    return JsonResponse({
        'games': list(res)
    })


@csrf_exempt
def getThemeList(request):
    res = queries.getThemeList().batch()
    print(res)
    return JsonResponse({
        'themes': list(res)
    })


@csrf_exempt
def getSummary(request):
    body = json.loads(request.body)
    gameKey = body['gameKey']

    if 'token' in body:
        token = body['token']
        user, newToken = util.getUserFromToken(token)
        if user is None:
            return util.returnError('Invalid token.', 401)
        
        print(gameKey, user['key'])
        res = queries.getSummary(gameKey, user['key']).batch()[0]
        return JsonResponse({
            'summary': res,
            'token': newToken
        })
    
    else:
        res = queries.getSummary(gameKey, '').batch()[0]
        print(res)
        return JsonResponse({
            'summary': res
        })


@csrf_exempt
def getDestination(request):
    body = json.loads(request.body)
    destKey = body['destKey']

    if 'token' in body:
        token = body['token']
        user, newToken = util.getUserFromToken(token)
        if user is None:
            return util.returnError('Invalid token.', 401)
        
        print(destKey, user['key'])
        res = queries.getDestination(destKey, user['key']).batch()[0]
        return JsonResponse({
            'summary': res,
            'token': newToken
        })
    
    else:
        res = queries.getDestination(destKey, user['key']).batch()[0]
        return JsonResponse({
            'summary': res
        })
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

@csrf_exempt
def incrementIndex(request):
    data = json.loads(request.body)
    print("data is " + str(data))
    connectionID = data['connectionID']
    queries.incrementIndex(connectionID)
    return JsonResponse({})

