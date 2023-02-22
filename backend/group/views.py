from django.http import JsonResponse
import json
import queries

# CONNECT: JOIN GAME
def connect(request):
    body = json.loads(request.body)
    print(request)
    return JsonResponse({})

def joinGame():
    return JsonResponse({})

# DISCONNECT:

def disconnect(request):
    print(request)
    return leaveGame(request)

def leaveGame(request):
    return JsonResponse({})

# DEFAULT

def default(request):
    body = json.loads(request.body)
    # match body.route:
    #     case ['update-game-settings']:
    #     case ['start-game']:
    #     case ['end-game']:


    return JsonResponse({})

# GET REQUEST: CREATE A LOBBY/GAME

def createGame(request):
    res = queries.createGame()
    return JsonResponse({'key': res['_key']})

    # startTime = json.loads(request.body)['startTime']
    # maxTime = json.loads(request.body)['maxTime']
    # intendedCompletionTime = json.loads(request.body)['intendedCompletionTime']

    # group = json.loads(request.body)['group']

    # destinations = json.loads(request.body)['destinations']

    # transportation = []
    # transportation.append(json.loads(request.body)['busAllowed'])
    # transportation.append(json.loads(request.body)['carAllowed'])
    # transportation.append(json.loads(request.body)['subwayAllowed'])
    # transportation.append(json.loads(request.body)['boatAllowed'])

    # radius = json.loads(request.body)['radius']

    # theme = json.loads(request.body)['theme']

    # res = queries.createLobby(startTime, maxTime, group, destinations, transportation, radius, intendedCompletionTime, theme)
