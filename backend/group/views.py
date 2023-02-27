from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import group.queries as queries
from ws_con import propogateUpdates, forceDisconnect

# CONNECT: JOIN GAME
@csrf_exempt
def onConnect(request):
    body = json.loads(request.body)
    gameKey = body['gameKey']
    userKey = body['userKey']
    connectionId = body['connectionId']
    print(gameKey, userKey, connectionId)
    res = queries.addPlayer(gameKey, userKey, connectionId)
    oldDoc = res.batch()[0]['oldDoc']
    if oldDoc:
        forceDisconnect(oldDoc['connectionId'])
    propogateAllUpdates(gameKey, { connectionId })
    return JsonResponse({})

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
    print(request)
    body = json.loads(request.body)
    print(body)
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

    # TRIGGER WEB-SCRAPER
    # result = getDestinations(settings)
    # EXAMPLE RESULT
    result = {
        'destinations': [],
        'trueCompletionTime': 0
    }

    res = queries.startGame(gameKey, settings)
    propogateAllUpdates(gameKey)
    return JsonResponse(res)

def propogateAllUpdates(gameKey, conExcl={}):
    data = queries.getGame(gameKey).batch()[0]
    users = data['users']
    game = data['game']
    propogateUpdates(users, str(game), conExcl)

# GET REQUEST: CREATE A LOBBY/GAME

def createGame(request):
    res = queries.createGame()
    print(res)
    return JsonResponse({'key': res['_key']})