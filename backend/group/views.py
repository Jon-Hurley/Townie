from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import group.queries as queries
from ws_con import propogateUpdates, forceDisconnect

# CONNECT: JOIN GAME
@csrf_exempt
def onConnect(request):
    # load input
    body = json.loads(request.body)
    gameKey = body['gameKey']
    token = body['token']
    connectionId = body['connectionId']
    lat = body['lat']
    lon = body['lon']
    print(gameKey, connectionId, lat, lon)

    userKey = "10010281"

    # add user to game, canceling their previous connection if left open
    res = queries.addPlayer(gameKey, userKey, connectionId, lat, lon)
    oldDoc = res.batch()[0]['oldDoc']
    if oldDoc:
        forceDisconnect(oldDoc['connectionId'])
    
    # relay game all game data to all players (except the new one)
    data = queries.getGame(gameKey).batch()[0]
    print(data)
    propogateAllUpdates(
        conExcl={ connectionId },
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
    if len(res): # a player was removed from DB.
        gameKey = res[0]['gameKey'][6:] # [6:] = id -> key
        propogateAllUpdates(gameKey, { connectionId })
    # else: connection was already updated, and no longer exists anyways.
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
        data = queries.getGame(gameKey).batch()[0]
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
        res = queries.updatePlayerLocation(connectionId, lon, lat).batch()[0]
        return JsonResponse({
            'method': 'update-location',
            'data': res
        })
    return JsonResponse({})

def propogateAllUpdates(gameKey=None, conExcl={}, data=None):
    if data is None:
        data = queries.getGame(gameKey).batch()[0]
    users = data['players']
    propogateUpdates(users, data, conExcl)

# GET REQUEST: CREATE A LOBBY/GAME

def createGame(request):
    res = queries.createGame().batch()[0]
    print(res)
    return JsonResponse({'key': res['_key']})

def getThemeList(request):
    res = queries.getThemeList().batch()
    print(res)
    return JsonResponse({ 'themes': list(res) })