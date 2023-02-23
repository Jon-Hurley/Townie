from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import group.queries as queries
from dotenv import load_dotenv
import os
import requests
load_dotenv()

# CONNECT: JOIN GAME
@csrf_exempt
def onConnect(request):
    body = json.loads(request.body)
    gameKey = body['gameKey']
    userKey = body['userKey']
    res = queries.addPlayer(gameKey, userKey)
    playerKey = res['_key']
    print("NEW GAME KEY:", gameKey)
    propogateAllUpdates(gameKey)
    return JsonResponse({
        'key': playerKey
    })

# DISCONNECT: LEAVE GAME
@csrf_exempt
def onDisconnect(request):
    body = json.loads(request.body)
    res = queries.leaveGame(body['playerKey'])
    propogateAllUpdates()
    print(request)
    return res

# DEFAULT:
#       1. Update Game Settings
#       2. Start Game
#       3. Update Location
@csrf_exempt
def default(request):
    body = json.loads(request.body)
    if body['route'] == 'update-game-settings':
        return updateGameSettings(body)
    if body['route'] == 'start-game':
        return startGame(body)
    if body['route'] == 'update-location':
        return updatePlayerLocation(body)
    return JsonResponse({ 'status': 'unknown route: ' + body['route'] })

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

# PROPOGATE CHANGES BACK TO USERS VIA WS API
# FUCK DJANGO AND ITS CONCURRENCY BS.

WS_API = os.environ.get('WS_ENDPOINT')

def propogateAllUpdates(gameKey):
    data = queries.getGame(gameKey).batch()[0]
    users = data['users']
    game = data['game']
    for user in users:
        propogateToOne(user, game)

def propogateToOne(user, game):
    print("Propogating to user")
    res = requests.post(
        WS_API + 'update/',
        json={
            'game': game,
            'userKey': user['key']
        }
    )
    print(res)

# GET REQUEST: CREATE A LOBBY/GAME

def createGame(request):
    res = queries.createGame()
    print(res)
    return JsonResponse({'key': res['_key']})