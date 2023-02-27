import arango_con
import time

def createGame():
    return arango_con.gameCollection.insert({
        'page': 'lobby',
        'startTime': 0,
        'maxTime': 0,
        'numFinished': 0,
        'trueCompletionTime': 0,
        'settings': {
            'radius': 5,
            'busAllowed': True,
            'carAllowed': True,
            'subwayAllowed': True,
            'boatAllowed': True,
            'theme': "None",
            'desiredCompletionTime': 180,
            'lon': 0.0,
            'lat': 0.0
        }
    })

def addPlayer(gameKey, userKey, connectionId):
    # return arango_con.playerCollection.insert({
    #     '_from': 'User/' + str(userKey),
    #     '_to': 'Games/' + str(gameKey),
    #     'connectionId': connectionId,
    #     'lon': 0,
    #     'lat': 0
    # })
    return arango_con.db.aql.execute(
        """
            UPSERT {
                _from: CONCAT("User/", @userKey)
            }
            INSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Games/", @gameKey),
                connectionId: @connectionId,
                lon: 0,
                lat: 0
            }
            UPDATE {
                _to: CONCAT("Games/", @gameKey),
                connectionId: @connectionId
            }
            IN Players
            RETURN {
                oldDoc: OLD
            }
        """,
        bind_vars={
            'gameKey': str(gameKey),
            'userKey': str(userKey),
            'connectionId': str(connectionId)
        }
    )

def leaveGame(connectionId):
    return arango_con.db.aql.execute(
        """
            FOR p IN Players
                FILTER p.connectionId == @connectionId
                
                LET gameKey = p._to
                REMOVE p._key in Players
                RETURN { gameKey }
        """,
        bind_vars={
            'connectionId': str(connectionId)
        }
    )

def startGame(gameKey, settings):
    # GET GAME SETTINGS
    # lobbyRes = lobbyCollection.get({
    #     '_key': gameKey
    # });
    # settings = lobbyRes['settings']

    # TRIGGER WEB-SCRAPER: (get destinations & auto add to the DB)
    # trueCompletionTime = WEB-SCRAPER(gameKey, settings)
    trueCompletionTime = 100

    t = time.time()
    return arango_con.gameCollection.update({
        '_key': gameKey,
        'page': 'map',
        'startTime': t,
        'maxTime': t + 24 * 60 * 60, # REPLACE W/ TTL index.
        'trueCompletionTime': trueCompletionTime
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
                        connectionId: e.connectionId,
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