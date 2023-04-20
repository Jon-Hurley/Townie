from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import group.queries as queries
import ws_con
import util
import time
import asyncio

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
    user, newToken = util.decodeUserJWT(token)
    if user is None:
        return util.returnError('Invalid token.', 401)
    
    userKey = user['key']

    # prune old connection ids for this user
    oldConnectionIds = queries.getUserConnectionIds(userKey).batch()
    for oldConnectionId in list(oldConnectionIds):
        if oldConnectionId != connectionId:
            ws_con.forceDisconnect(oldConnectionId)

    # add user to game, nulling their previous connection if left open
    res = queries.addPlayer(gameKey, userKey, connectionId, lat, lon).batch()

    # relay game all game data to all players (except the new one)
    propogateAllUpdates(gameKey, conExlusion={connectionId})

    # send game data to new player
    return JsonResponse({})

# DISCONNECT: LEAVE GAME


@csrf_exempt
def onDisconnect(request):
    body = json.loads(request.body)
    connectionId = body['connectionId']
    print(connectionId)
    res = queries.leaveGame(connectionId).batch()
    if len(res):
        gameKey = res[0]['gameId'][6:]  # [6:] = id -> key
        propogateAllUpdates(gameKey)
        
    return JsonResponse({})


@csrf_exempt
def onDefault(request):
    data = json.loads(request.body)
    connectionId = data['connectionId']
    body = data['body']
    method = body['method']
    # print(method, connectionId, body)

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
    
    if method == 'new-message':
        token = body['token']
        connectionIds = body['connectionIds']

        user = util._decodeUserJWT(token)
        messageObj = {
            'message': body['message'],
            'key': user['key'],
            'username': user['username'],
            'isPremium': user['isPremium'],
            'timestamp': int(time.time() * 1000)
        }
        asyncio.run(
            ws_con.propogateToUsers(
                connectionIds,
                data = json.dumps({
                    'method': 'new-message',
                    'data': messageObj
                })
            )
        )
        return JsonResponse({})

    if method == 'update-location':
        lon = body['lon']
        lat = body['lat']
        gameKey = body['gameKey']

        for i in range(3):
            try:
                res = queries.updatePlayerLocation(
                    connectionId, lon, lat
                ).batch()[0]
                break
            except Exception as err:
                print(err)
            
        propogateAllUpdates(gameKey)

        return JsonResponse({
            'method': 'update-location',
            'data': res
        })
    
    return JsonResponse({})


def propogateAllUpdates(gameKey=None, data=None, conExlusion={}):
    if data is None:
        data = queries.getGame(gameKey).batch()[0]
    
    asyncio.run(
        ws_con.propogateToPlayers(data, conExlusion)
    )


# NOTE: ALL HTTP REQUESTS BELOW ARE FOR IN-GAME USE ONLY

@csrf_exempt
def createGame(request):
    data = json.loads(request.body)
    lon = data['lon']
    lat = data['lat']

    user, newToken = util.decodeUserJWT(data['token'])
    if user is None:
        return util.returnError('Invalid token', 401)

    res = queries.createGame(lon, lat).batch()[0]
    print(res)
    return JsonResponse({
        'key': res['_key'],
        'token': newToken
    })

@csrf_exempt
def getGame(request):
    data = json.loads(request.body)
    print(data)
    gameKey = data['gameKey']
    data = queries.getGame(gameKey).batch()[0]
    return JsonResponse(data)

# @csrf_exempt
# def getChatPermissions(request):
#     body = json.loads(request.body)
#     gameKey = body['gameKey']

#     user, newToken = util.decodeUserJWT(body['token'])
#     if user is None:
#         return util.returnError('Invalid token.', 401)

#     password = redis_con.createConnectionCredentials(user['key'], gameKey)
#     return JsonResponse({
#         'password': password,
#         'token': newToken
#     })