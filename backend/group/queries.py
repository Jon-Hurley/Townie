import arango_con
import time
from . import scraper

def createGame():
    return arango_con.db.aql.execute(
        """
        INSERT {
            page: 'lobby',
            createTime: DATE_NOW(),
            maxTime: DATE_NOW() + 24 * 60 * 60 * 1000,
            settings: {
                radius: 5,
                walkingAllowed: True,
                drivingAllowed: False,
                bicyclingAllowed: False,
                transitAllowed: False,
                theme: "restaurant",
                desiredCompletionTime: 180,
                budget: 1,
                lon: 0.0,
                lat: 0.0
            }
        }
        INTO Games
        RETURN NEW
        """
    )

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
                dist: 0,
                points: 0,
                lon: 0,
                lat: 0,
                totalDist: 0
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
    trueCompletionTime = scraper.generate(settings, gameKey)
    #trueCompletionTime = 100

    return arango_con.db.aql.execute(
        """
            LET t = DATE_NOW()

            FOR p IN Players
                FILTER p._to == CONCAT('Games/', @gameKey)
                UPDATE p
                WITH {
                    prevTime: t,
                    time: 0,
                    totalTime: 0,
                    paused: false
                }
                IN Players

            UPDATE @gameKey
            WITH {
                page: 'map',
                trueCompletionTime: @trueCompletionTime,
                startTime: t
            }
            IN Games
            RETURN NEW           
        """,
        bind_vars={
            'gameKey': str(gameKey),
            'trueCompletionTime': trueCompletionTime
        }
    )



def updateGameSettings(gameKey, settings):
    updates = {
        '_key': gameKey,
        'settings': settings
    }
    return arango_con.gameCollection.update(updates, return_new=True)

def updatePlayerLocation(connectionId, lon, lat):
    return arango_con.db.aql.execute(
        """
        WITH Destinations

        FOR p IN Players
            FILTER p.connectionId == @connectionId
            
            LET delta = p.lat ? DISTANCE(p.lat, p.lon, @lat, @lon) : 0
            
            LET destDelta = (
                FOR v, e IN 1..1 OUTBOUND p._to Itineraries
                    FILTER e.index == p.destinationIndex
                    LET dist = DISTANCE(v.latitude, v.longitude, @lat, @lon)
                    LET inc = (dist != NULL && dist < 20)
                    RETURN {
                        inc,
                        points: e.points * inc
                    }
            )[0]

            LET t = DATE_NOW()
            LET dt = (1 - p.paused) * (t - p.prevTime)

            UPDATE p
            WITH {
                lon: @lon,
                lat: @lat,
                
                dist: (p.dist + delta) * (1 - destDelta.inc),
                totalDist: p.totalDist + delta,
                destinationIndex: p.destinationIndex + destDelta.inc,
                points: p.points + destDelta.points,
                
                prevTime: t,
                time: (p.time + dt) * (1 - destDelta.inc),
                totalTime: p.totalTime + dt
            }
            IN Players
            RETURN {
                destinationIndex: NEW.destinationIndex,
                time: OLD.time
            }
        """,
        bind_vars={
            'connectionId': str(connectionId),
            'lon': lon,
            'lat': lat
        }
    )

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
        searcher = dict(name=listDict['Destinations'][i]['destination']['name'])
        destination = arango_con.destinationCollection.find(searcher)
        destination1 = [doc for doc in destination]
        arango_con.db.aql.execute(
            """
        UPSERT {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points,
            timeToCompletion: @time
        }
        INSERT {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points,
            timeToCompletion: @time
        }
        UPDATE {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points,
            timeToCompletion: @time
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
                'points': 11,
                'time': listDict['Destinations'][i]['time']
            }
        )

def insertIntoUnusedItinerary(listDict, gameKey, index):
    for i in range(len(listDict)):
        searcher = dict(name=listDict[i]['name'])
        destination = arango_con.destinationCollection.find(searcher)
        destination1 = [doc for doc in destination]
        arango_con.db.aql.execute(
            """
        UPSERT {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points,
        }
        INSERT {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points,
        }
        UPDATE {
            _from: @gameKey,
            _to: @DestKey,
            index: @index,
            points: @points,
        }
        IN UnusedItineraries
        RETURN {
            oldDoc: OLD
        }
        """,
            bind_vars={
                'gameKey': "Games/" + str(gameKey),
                'DestKey': destination1[0]['_id'],
                'index': index + i,
                'points': 11,
            }
        )