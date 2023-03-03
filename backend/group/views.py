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
    userKey = body['userKey']
    connectionId = body['connectionId']
    print(gameKey, userKey, connectionId)

    # add user to game, canceling their previous connection if left open
    res = queries.addPlayer(gameKey, userKey, connectionId)
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

# DEFAULT: (right now will be done in http requests lol)
#       1. Update Game Settings
#       2. Start Game
#       3. Update Location
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
        return JsonResponse(data)
    
    if method == 'update-settings':
        gameKey = body['gameKey']
        settings = body['settings']
        print(gameKey, settings)
        res = queries.updateGameSettings(gameKey, settings)
        print(res)
        propogateAllUpdates(gameKey)
        return JsonResponse({})

    if method == 'start-game':
        gameKey = body['gameKey']
        settings = body['settings']
        res = queries.startGame(gameKey, settings)
        return(res)
        # print("HELLO", gameKey)
    # print(data)
    # propogateAllUpdates(
    #     conExcl={ connectionId },
    #     data=data
    # )
    
    # body = json.loads(request.body)
    # print(request.POST)
    # print(request.GET)
    # if body['action'] == 'update-game-settings':
    #     return updateGameSettings(body)
    # if body['action'] == 'start-game':
    #     return startGame(body)
    # if body['action'] == 'update-location':
    #     return updatePlayerLocation(body)
    return JsonResponse({})

def updatePlayerLocation(body):
    playerKey = body['key']
    lon = body['lon']
    lat = body['lat']
    res = queries.updatePlayerLocation(playerKey, lon, lat)
    return JsonResponse(res)

def updateGameSettings(body):
    playerKey = body['key']
    field = body['field']
    value = body['value']

    res = queries.updatePlayerLocation(playerKey, field, value)
    return JsonResponse(res)

def startGame(body):
    gameKey = body['gameKey']
    settings = body['settings']
    res = queries.startGame(gameKey, settings)
    propogateAllUpdates(gameKey)
    return JsonResponse(res)

def propogateAllUpdates(gameKey=None, conExcl={}, data=None):
    if data is None:
        data = queries.getGame(gameKey).batch()[0]
    users = data['players']
    propogateUpdates(users, data, conExcl)

# GET REQUEST: CREATE A LOBBY/GAME

def createGame(request):
    res = queries.createGame()
    print(res)
    return JsonResponse({'key': res['_key']})