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
                theme: "None",
                desiredCompletionTime: 180,
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
            LET oldConnectionIds = (
                FOR v, e
                IN 1..1
                ANY CONCAT("User/", @userKey)
                GRAPH Playerships
                    FILTER e.connectionId != null
                    RETURN e.connectionId
            )

            UPSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Games/", @gameKey)
            }
            INSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Games/", @gameKey),
                connectionId: @connectionId,
                destinationIndex: 0,
                lon: 0,
                lat: 0,
                time: 0,
                dist: 0,
                totalDist: 0,
                totalTime: 0,
                points: 0,
                addedPoints: 0,
                finished: false,
                paused: false
            }
            UPDATE {
                connectionId: @connectionId,
                finished: false
            }
            IN Players

            RETURN oldConnectionIds
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
                    && p.connectionId != null

                LET u = (
                    FOR u in User
                        FILTER u._id == p._from
                        UPDATE u
                        WITH {
                            points: p.points - p.addedPoints
                        }
                        IN User
                        RETURN NEW
                )
        
                UPDATE p
                WITH {
                    finished: true,
                    connectionId: null,
                    addedPoints: p.points
                }
                IN Players
                RETURN {
                    gameId: OLD._to
                }
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
    trueCompletionTime = scraper.map(settings, gameKey)
    # trueCompletionTime = 100

    return arango_con.db.aql.execute(
        """
            LET t = DATE_NOW()

            FOR p IN Players
                FILTER p._to == CONCAT('Games/', @gameKey)
                    && p.connectionId != null
                UPDATE p
                WITH {
                    prevTime: t
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
                && p.connectionId != null
            
            LET atPrevDest = (
                FOR v, e IN 1..1 OUTBOUND p._to Itineraries
                    FILTER e.index == p.destinationIndex - 1
                    LET dist = DISTANCE(v.latitude, v.longitude, @lat, @lon)
                    LET inc = (dist != NULL && dist < 20)
                    RETURN inc
            )[0] // WHETHER PLAYER IS STILL AT PREV DEST
            
            LET destDelta = (
                FOR v, e IN 1..1 OUTBOUND p._to Itineraries
                    FILTER e.index == p.destinationIndex
                    LET dist = DISTANCE(v.latitude, v.longitude, @lat, @lon)
                    LET inc = (dist != NULL && dist < 20)
                    RETURN {
                        inc,
                        points: e.points * inc
                    }
            )[0] // HAS PLAYER REACHED NEXT DEST
            
            // NO dt/dx UPDATES IF PAUSED, STILL AT PREV DEST, OR DONE
            LET notQuiet = !(p.paused || atPrevDest || destDelta != NULL)
            // RESET TIME AND DIST ON DESTINATION ARRIVAL
            LET notArrived = !destDelta.inc
            
            LET t = DATE_NOW()
            LET dt = (t - p.prevTime) * notQuiet
            LET dx = p.lat ? DISTANCE(p.lat, p.lon, @lat, @lon) * notQuiet : 0
            
            UPDATE p
            WITH {
                lon: @lon,
                lat: @lat,
                
                dist: (p.dist + dx) * notArrived,
                totalDist: p.totalDist + dx,
                destinationIndex: p.destinationIndex + destDelta.inc,
                points: p.points + destDelta.points,
                
                prevTime: t,
                time: (p.time + dt) * notArrived,
                totalTime: p.totalTime + dt
            }
            IN Players
            RETURN {
                destinationIndex: OLD.destinationIndex,
                reached: destDelta.inc,
                quiet: !notQuiet,
                time: OLD.time,
                dist: OLD.dist,
                totalTime: OLD.totalTime,
                totalDist: OLD.totalDist
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
                FILTER e.connectionId != null
                RETURN {
                    key: v._key,
                    username: v.username,
                    connectionId: e.connectionId,
                    lon: e.lon,
                    lat: e.lat,
                    destinationIndex: e.destinationIndex,
                    points: e.points
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

def getGameForPlayer(gameKey, connectionId):
    return arango_con.db.aql.execute(
        """
        WITH User, User, Destinations

        LET players = (
            FOR v, e IN 1..1 INBOUND CONCAT("Games/", @key) Players
                FILTER e.connectionId != null
                RETURN {
                    key: v._key,
                    username: v.username,
                    connectionId: e.connectionId,
                    lon: e.lon,
                    lat: e.lat,
                    destinationIndex: e.destinationIndex,
                    points: e.points
                }
        )

        LET player = (
            FOR v, e IN 1..1 INBOUND CONCAT("Games/", @key) Players
                FILTER e.connectionId == @connectionId
                RETURN {
                    key: v._key,
                    username: v.username,
                    connectionId: e.connectionId,
                    lon: e.lon,
                    lat: e.lat,
                    destinationIndex: e.destinationIndex,
                    points: e.points
                }
        )[0]

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
            destinations,
            player
        }
    """,
        bind_vars={
            'key': str(gameKey),
            'connectionId': str(connectionId)
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
    # technially deprecated
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
