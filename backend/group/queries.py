import arango_con
import time

def createGame():
    return arango_con.gameCollection.insert({
        'page': 'lobby',
        'startTime': 0,
        'maxTime': 0,
        'numFinished': 0,
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

def addPlayer(gameKey, userKey):
    return arango_con.playerCollection.insert({
        '_from': 'User/' + str(userKey),
        '_to': 'Games/' + str(gameKey),
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

def updatePlayerLocation(playerKey, lon, lat):
    updates = {
        '_key': playerKey,
        'lon': lon,
        'lat': lat
    }
    return arango_con.playerCollection.update(updates)


def getGame(gameKey):
    return arango_con.db.aql.execute(
        """
            WITH User

            LET users = (
                FOR v, e IN 1..1 ANY CONCAT("Games/", @key) Players
                    return {
                        key: v._key,
                        username: v.username,
                        lon: e.lon,
                        lat: e.lat
                    }
            )

            FOR game IN Games
                FILTER game._key == @key
                return {
                    game: game,
                    users: users
                }
        """,
        bind_vars={
            'key': str(gameKey),
        }
    )