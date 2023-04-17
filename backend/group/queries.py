import arango_con
import time
from . import scraper, scraperfsq

def createGame(lon, lat):
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
                lon: @lon,
                lat: @lat
            }
        }
        INTO Games
        RETURN NEW
        """,
        bind_vars={
            'lon': lon,
            'lat': lat
        }
    )


def addPlayer(gameKey, userKey, connectionId, lat, lon):
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
                time: 0,
                dist: 0,
                totalDist: 0,
                totalTime: 0,
                points: 0,
                addedPoints: 0,
                finished: false,
                paused: false,
                lon: @lon,
                lat: @lat,
                prevTime: DATE_NOW()
            }
            UPDATE {
                connectionId: @connectionId,
                finished: false,
                lon: @lon,
                lat: @lat,
                prevTime: DATE_NOW()
            }
            IN Players

            RETURN oldConnectionIds
        """,
        bind_vars={
            'gameKey': str(gameKey),
            'userKey': str(userKey),
            'connectionId': str(connectionId),
            'lat': float(lat),
            'lon': float(lon)
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
    trueCompletionTime = scraperfsq.generate(settings, gameKey)

    # IF NO DESTINATIONS FOUND, THROW ERROR
    if (trueCompletionTime == 0):
        raise Exception("No destinations found")
    
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
                    LET inc = (dist != NULL && dist < 50)
                    RETURN inc
            )[0] // WHETHER PLAYER IS STILL AT PREV DEST
            
            LET destDelta = (
                FOR v, e IN 1..1 OUTBOUND p._to Itineraries
                    FILTER e.index == p.destinationIndex
                    LET dist = DISTANCE(v.latitude, v.longitude, @lat, @lon)
                    LET inc = (dist != NULL && dist < 50)
                    RETURN {
                        inc,
                        points: e.points,
                        trueTime: e.timeToCompletion
                    }
            )[0] // HAS PLAYER REACHED NEXT DEST

            LET newDestDelta = destDelta ? destDelta : { inc: 0, points: 0, trueTime: 1 }

            // NO dt/dx UPDATES IF PAUSED, STILL AT PREV DEST, OR DONE
            LET quiet = p.paused || atPrevDest || (destDelta == NULL)
            // RESET TIME AND DIST ON DESTINATION ARRIVAL
            LET arrived = newDestDelta.inc
            
            LET t = DATE_NOW()
            LET dt = quiet ? 0 : (t - p.prevTime)
            LET dx = quiet ? 0 : DISTANCE(p.lat, p.lon, @lat, @lon)

            LET newTime = p.time + dt
            LET newTimeSec = newTime / 1000
            LET pMult = 1 - (newTimeSec / newDestDelta.trueTime) / 2
            LET dp = arrived ? 
                MAX(
                    [ROUND(MAX([pMult, 0]) * newDestDelta.points),
                    0]
                )
                : 0

            UPDATE p
            WITH {
                lon: @lon,
                lat: @lat,
                prevTime: t,

                destinationIndex: p.destinationIndex + arrived,
                points: p.points + dp,
                dist: arrived ? 0 : p.time + dx,
                time: arrived ? 0 : p.time + dt,
                totalDist: p.totalDist + dx,
                totalTime: p.totalTime + dt
            }
            IN Players
            RETURN {
                newTime: NEW.time,
                newDist: NEW.dist,
                oldTime: OLD.time,
                oldDist: OLD.dist,

                totalTime: NEW.totalTime,
                totalDist: NEW.totalDist,

                quiet,
                arrived,

                atPrevDest: atPrevDest || arrived,
                potentialPoints: dp,
                points: newDestDelta.points,
                trueCompletionTime: newDestDelta.trueTime,
                destDelta
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
                    lon: v.hidingState ? null : e.lon,
                    lat: v.hidingState ? null : e.lat,
                    destinationIndex: e.destinationIndex,
                    points: e.points,
                    hidingState: v.hidingState
                }
        )

        LET destinations = (
            FOR v, e IN 1..1 OUTBOUND CONCAT("Games/", @key) Itineraries
                RETURN {
                    index: e.index,
                    points: e.points,
                    timeToCompletion: e.timeToCompletion,
                    name: v.name,
                    lon: v.longitude,
                    lat: v.latitude,
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


def getSummary(gameKey):
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
                    lat: e.lat,
                    destinationIndex: e.destinationIndex,
                    points: e.points,
                    hidingState: v.hidingState
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
                    lon: v.hidingState ? null : e.lon,
                    lat: v.hidingState ? null : e.lat,
                    destinationIndex: e.destinationIndex,
                    points: e.points,
                    hidingState: v.hidingState
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
                    points: e.points,
                    hidingState: v.hidingState
                }
        )[0]

        LET destinations = (
            FOR v, e IN 1..1 OUTBOUND CONCAT("Games/", @key) Itineraries
                RETURN {
                    index: e.index,
                    points: e.points,
                    timeToCompletion: e.timeToCompletion,
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


def createDestination(lat, lng, name, theme, tips):
    
    # list = [lat, lng]
    # arango_con.destinationCollection.insert(
    #     {
    #     'latitude': lat,
    #     'longitude': lng,
    #     'name': name,
    #     'theme': theme,
    #     'tips': [tips]
    #     }, 
    #     False, 
    #     True, 
    #     True, 
    #     True, 
    #     False, 
    #     "update"
    # )
    arango_con.db.aql.execute(
            """
        UPSERT {
            name: @name
        }
        INSERT {
            name: @name,
            latitude: @lat,
            longitude: @lng,
            theme: @theme,
            tips: @tips,
            rating: 0,
            numRatings: 0
        }
        UPDATE {
            name: @name,
            latitude: @lat,
            longitude: @lng,
            theme: @theme,
            tips: @tips,
        }
        IN Destinations
        RETURN {
            oldDoc: OLD
        }
        """,
            bind_vars={
                'name': name,
                'lat': lat,
                'lng': lng,
                'theme': theme,
                'tips': tips
            }
        )


def getNearbyDestinations(lat, lng, radius, theme):
    return arango_con.db.aql.execute(
        """
        FOR x IN Destinations
            FILTER GEO_DISTANCE([@lat, @lng], [x.latitude, x.longitude]) <= @radius
            FILTER GEO_DISTANCE([@lat, @lng], [x.latitude, x.longitude]) >= 100
            FILTER x.theme == @theme
            LIMIT 50
            RETURN x
        """,
        bind_vars={
            'lat': lat,
            'lng': lng,
            'radius': radius,
            'theme': theme
        }
    )


def insertIntoItinerary(listDict, gameKey):
    for i in range(len(listDict['Destinations'])):
        searcher = dict(name=listDict['Destinations']
                        [i]['destination']['name'])
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
                'points': 1000,
                'time': listDict['Destinations'][i]['time']
            }
        )


def insertIntoNewItinerary(listDict, gameKey, index):
    for i in range(len(listDict['Destinations'])):
        searcher = dict(name=listDict['Destinations']
                        [i]['destination']['name'])
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
                'index': i + index,
                'points': 1000,
                'time': listDict['Destinations'][i]['time']
            }
        )


def insertIntoUnusedItinerary(listDict, gameKey):
    for i in range(len(listDict)):
        searcher = dict(name=listDict[i]['name'])
        destination = arango_con.destinationCollection.find(searcher)
        destination1 = [doc for doc in destination]
        arango_con.db.aql.execute(
            """
        UPSERT {
            _from: @gameKey,
            _to: @DestKey,
            points: @points,
        }
        INSERT {
            _from: @gameKey,
            _to: @DestKey,
            points: @points,
        }
        UPDATE {
            _from: @gameKey,
            _to: @DestKey,
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
                'points': 11,
            }
        )


def findUnusedItineraries(gameKey):
    itineraries = arango_con.unusedItineraryCollection.find(
        dict(_from="Games/" + str(gameKey)))
    itineraries1 = [doc for doc in itineraries]
    return itineraries1


def findUnusedDestsFromItinerary(listDict):
    list = []
    for i in range(len(listDict)):
        destinations = arango_con.destinationCollection.find(
            dict(_id=listDict[i]['_to']))
        destinations1 = [doc for doc in destinations]
        list.append(destinations1[0])
    return list


def findPlayers(gameKey):
    players = arango_con.playerCollection.find(
        dict(_to="Games/" + str(gameKey)))
    players1 = [doc for doc in players]
    return players1


def removeUnusedItinerary(itinerary, gameKey):
    old_itinerary = arango_con.unusedItineraryCollection.delete_match(
        dict(_to=itinerary['_id'], _from="Games/" + str(gameKey)))

# def getHighestIndex(gameKey):
#     game = arango_con.gameCollection.find(dict(_id=("Games/" + str(gameKey))))
#     game1 = [doc for doc in game]
#     edges = arango_con.itineraryCollection.edges(game1[0]['game']['_id'])
#     edges1 = [doc for doc in edges]
#     num_index = len(edges1)
#     return num_index

# def getItinerary(game):
#     print(game)
#     edges = arango_con.itineraryCollection.edges(game['game']['_id'])
#     edges1 = [doc for doc in edges]
#     return edges1


def updateTrueTime(gameKey, settings):
    new_desired_time = settings['desiredCompletionTime']
    game = arango_con.gameCollection.find(dict(_id=("Games/" + str(gameKey))))
    game1 = [doc for doc in game]

    new_true_time = 0
    if new_desired_time < game1[0]['settings']['desiredCompletionTime']:
        print("decrease")
        new_true_time = scraperfsq.truncateGame(settings, gameKey)
    elif new_desired_time > game1[0]['settings']['desiredCompletionTime']:
        print("increase")
        new_true_time = scraperfsq.extendGame(settings, gameKey)
    game1[0]['settings'] = settings
    game1[0]['trueCompletionTime'] = new_true_time
    return arango_con.gameCollection.update_match(dict(_key=game1[0]['_key']), game1[0])


def removeItinerary(itinerary, gameKey):
    arango_con.itineraryCollection.delete_match(
        dict(index=itinerary['index'], _from="Games/" + str(gameKey)))


def getItinerary(gameKey):
    return arango_con.db.aql.execute(
        """
            WITH Destinations

            LET destinations = (
                FOR v, e IN 1..1 OUTBOUND CONCAT("Games/", @key) Itineraries
                    RETURN {
                        index: e.index,
                        points: e.points,
                        timeToCompletion: e.timeToCompletion,
                        name: v.name,
                        lon: v.longitude,
                        lat: v.latitude
                    }
            )
            RETURN {
                destinations
            }
        """,
        bind_vars={
            'key': str(gameKey),
        }
    )


def getThemeList():
    return arango_con.db.aql.execute(
        """
        FOR theme IN Themes
            SORT theme.rating DESC
            RETURN {
                'theme': theme.name
            }
        """
    )
