from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import group.queries as queries
from ws_con import propogateUpdates, forceDisconnect
import util

# CONNECT: JOIN GAME


@csrf_exempt
def onConnect(request):
    # load input

    input = request.body.decode('utf8').replace("\r", '').replace("\n", '')
    print(input)
    body = json.loads(input)
    gameKey = body['gameKey']
    token = body['token']
    connectionId = body['connectionId']
    lat = body['lat']
    lon = body['lon']
    print(gameKey, token, connectionId, lat, lon)

    # get user key from token
    user, newToken = util.getUserFromToken(token)
    if user is None:
        return util.returnError('Invalid token.', 401)

    userKey = user['key']

    # add user to game, nulling their previous connection if left open
    res = queries.addPlayer(gameKey, userKey, connectionId, lat, lon)
    oldConnectionIds = res.batch()[0]
    print(oldConnectionIds)
    for oldConnectionId in oldConnectionIds:
        try:
            forceDisconnect(oldConnectionId)
        except Exception as err:
            print(err)

    # relay game all game data to all players (except the new one)
    data = queries.getGame(gameKey).batch()[0]
    print(data)
    propogateAllUpdates(
        conExcl={connectionId},
        data=data
    )

    # send game data to new player
    return JsonResponse(data)

# DISCONNECT: LEAVE GAME


@csrf_exempt
def onDisconnect(request):
    body = json.loads(request.body)
    connectionId = body['connectionId']
    print(connectionId)
    res = queries.leaveGame(connectionId).batch()
    if len(res):
        gameKey = res[0]['gameId'][6:]  # [6:] = id -> key
        propogateAllUpdates(gameKey, {connectionId})
    return JsonResponse({})


@csrf_exempt
def onDefault(request):
    data = json.loads(request.body)
    connectionId = data['connectionId']
    body = data['body']
    print(connectionId, body)
    method = body['method']

    if method == 'get-game':
        gameKey = body['gameKey']
        data = queries.getGameForPlayer(gameKey, connectionId).batch()[0]
        return JsonResponse({
            'method': 'get-game',
            'data': data
        })

    if method == 'update-settings':
        gameKey = body['gameKey']
        settings = body['settings']

        print(gameKey, settings)
        res = queries.updateGameSettings(gameKey, settings)
        print(res)
        propogateAllUpdates(gameKey)
        return JsonResponse({
            'method': 'update-settings'
        })

    if method == 'update-time':
        gameKey = body['gameKey']
        settings = body['settings']
        print(gameKey, settings)
        res = queries.updateTrueTime(gameKey, settings)
        print(res)
        propogateAllUpdates(gameKey)
        return JsonResponse({
            'method': 'update-time'
        })

    if method == 'start-game':
        gameKey = body['gameKey']
        settings = body['settings']
        res = queries.startGame(gameKey, settings).batch()[0]
        propogateAllUpdates(gameKey)
        return JsonResponse({
            'method': 'start-game'
        })

    if method == 'update-location':
        lon = body['lon']
        lat = body['lat']

        for i in range(3):
            try:
                res = queries.updatePlayerLocation(connectionId, lon, lat).batch()[0]
                break
            except Exception as err:
                print(err)

        return JsonResponse({
            'method': 'update-location',
            'data': res
        })
    return JsonResponse({})


def propogateAllUpdates(gameKey=None, conExcl={}, data=None):
    if data is None:
        data = queries.getGame(gameKey).batch()[0]
    propogateUpdates(data, conExcl)

# GET REQUEST: CREATE A LOBBY/GAME


@csrf_exempt
def createGame(request):
    data = json.loads(request.body)
    lon = data['lon']
    lat = data['lat']

    user, newToken = util.getUserFromToken(data['token'])
    if user is None:
        return util.returnError('Invalid token', 401)
    
    res = queries.createGame(lon, lat).batch()[0]
    print(res)
    return JsonResponse({
        'key': res['_key'],
        'token': newToken
    })

# GET REQUEST: GET GAME DATA


@csrf_exempt
def getGame(request):
    data = json.loads(request.body)
    print(data)
    gameKey = data['gameKey']
    data = queries.getGame(gameKey).batch()[0]
    return JsonResponse(data)


def getThemeList(request):
    res = queries.getThemeList().batch()
    print(res)
    return JsonResponse({'themes': list(res)})


@csrf_exempt
def getSummary(request):
    data = json.loads(request.body)
    print(data)
    gameKey = data['gameKey']
    data = queries.getSummary(gameKey).batch()[0]
    return JsonResponse(data)
