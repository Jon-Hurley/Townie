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
            'walkingAllowed': True,
            'drivingAllowed': False,
            'bicyclingAllowed': False,
            'transitAllowed': False,
            'theme': "None",
            'desiredCompletionTime': 180,
            'lon': 0.0,
            'lat': 0.0
        }
    })

def addPlayer(gameKey, userKey, connectionId):
    return arango_con.db.aql.execute(
        """
            UPSERT {
                _from: CONCAT("User/", @userKey)
            }
            INSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Games/", @gameKey),
                connectionId: @connectionId,
                destinationIndex: 0,
                points: 0,
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
    
def updateGameSettings(gameKey, settings):
    updates = {
        '_key': gameKey,
        'settings': settings
    }
    return arango_con.gameCollection.update(updates, return_new=True)

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
            WITH User, Destinations

            LET players = (
                FOR v, e IN 1..1 INBOUND CONCAT("Games/", @key) Players
                    RETURN {
                        key: v._key,
                        username: v.username,
                        connectionId: e.connectionId,
                        lon: e.lon,
                        lat: e.lat
                    }
            )

            LET destinations = (
                FOR v, e IN 1..1 OUTBOUND CONCAT("Games/", @key) Itineraries
                    RETURN {
                        index: e.index,
                        points: e.points,
                        name: v.name,
                        lon: v.longitude,
                        lat: v.latitude
                    }
            )

            FOR game IN Games
                FILTER game._key == @key
                RETURN {
                    game,
                    players,
                    destinations
                }
        """,
        bind_vars={
            'key': str(gameKey),
        }
    )

def createDestination(lat, lng, name, theme):
    try:
        list = [lat, lng]
        return arango_con.destinationCollection.insert({
    'latitude': lat,
    'longitude': lng,
    'name': name,
    'theme': theme
    })
    except:
        pass

def getNearbyDestinations(lat, lng, radius):
    #technially deprecated
    return arango_con.destinationCollection.find_in_radius(lat, lng, radius/0.000621371)

def insertIntoItinerary(listDict, gameKey):
    for i in range(len(listDict['Destinations'])):
        searcher = dict(name=listDict['Destinations'][i]['name'])
        destination = arango_con.destinationCollection.find(searcher)
        destination1 = [doc for doc in destination]
        arango_con.db.aql.execute(
        """
        UPSERT {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points
        }
        INSERT {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points
        }
        UPDATE {
            _from: @gameKey,
            _to: @DestKey,
            points: @points
        }
        IN Itineraries
        RETURN {
            oldDoc: OLD
        }
        """,
            bind_vars={
                'gameKey': "Games/" + str(gameKey),
                'DestKey': destination1[0]['_id'],
                'index': i,
                'points': 11
            }
        )