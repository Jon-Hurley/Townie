import arango_con
import time

def createGame():
    return arango_con.gameCollection.insert({
        'page': 'lobby',
        'startTime': 0,
        'maxTime': 0,
        'numFinished': 0,
        'members': [],
        'destinations': [],
        'trueCompletionTime': 0,
        'settings': {
            'radius': 5,
            'busAllowed': True,
            'carAllowed': True,
            'subwayAllowed': True,
            'boatAllowed': True,
            'theme': "None",
            'desiredCompletionTime': 180
        }
    })

def joinGame(gameKey, userKey):
    return arango_con.playerCollection.insert({
        '_from': gameKey,
        '_to': userKey,
        'lon': 0,
        'lat': 0
    })

def leaveGame(playerKey):
    return arango_con.playerCollection.delete({
        '_key': playerKey
    })

def startGame(gameKey, settings):
    # lobbyRes = lobbyCollection.get({
    #     '_key': gameKey
    # });
    # settings = lobbyRes['settings']

    # TRIGGER WEB-SCRAPER
    # result = getDestinations(settings)
    
    # EXAMPLE RESULT
    result = {
        'destinations': [],
        'trueCompletionTime': 0
    }

    t = time.time()
    return arango_con.gameCollection.update({
        '_key': gameKey,
        'page': 'map',
        'startTime': t,
        'maxTime': t + 24 * 60 * 60,
        'destinations': result['destinations'],
        'trueCompletionTime': result['trueCompletionTime']
    })
    
def updateGameSettings(gameKey, field, value):
    updates = {
        '_key': gameKey
    }
    updates[field] = value
    return arango_con.gameCollection.update(updates)