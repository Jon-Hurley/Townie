from arango import ArangoClient
from dotenv import load_dotenv
import os
import time

load_dotenv()

host = os.environ.get('ARANGO_ENDPOINT')
password = os.environ.get('ARANGO_PASSWD')

client = ArangoClient(hosts=[host])
db = client.db('_system', username='root', password=password)

userCollection = db.collection('User')
friendsCollection = db.collection('Friends')
lobbyCollection = db.collection('Lobbies')

def createUser(username, password, phoneNumber):
    return userCollection.insert({
        'username': username,
        'passwordHash': password,
        'phone': phoneNumber,
        'points': 0,
        'rank': 'beginner',
        'purchases': []
    })

def getUser(userKey, targetKey):
    return db.aql.execute(
        """
        LET userId = CONCAT("User/", @userKey)

        LET f = (
            FOR v, e IN 1..1 ANY userId Friends
                FILTER v._key == @targetKey
                return {
                    status: e.status,
                    'inbound': e._to == userId,
                    key: e._key
                }
        )

        FOR user IN User
            FILTER user._key == @targetKey
            RETURN {
                key: user._key,
                rank: user.rank,
                username: user.username,
                points: user.points,
                purchases: user.purchases,
                friendship: f
            }
        """,
        bind_vars={
            'targetKey': targetKey,
            'userKey': userKey
        }
    )

def getUsersBySubstring(substr):
    return db.aql.execute(
        """
        FOR user IN User
            LET x = CONTAINS(LOWER(user.username), LOWER(@substr), true)
            SORT x
            FILTER x != -1
            LIMIT 10
            RETURN {
                key: user._key,
                username: user.username
            }
        """,
        bind_vars={'substr': substr}
    )

def getFriendsList(key):
    return db.aql.execute(
        """
        WITH User
        FOR v, e IN 1..1 ANY CONCAT("User/", @key) Friends
            FILTER e.status
            RETURN {
                key: v._key,
                username: v.username
            }
        """,
        bind_vars={'key': key} 
    )

def getPendingFriendsList(key):
    return db.aql.execute(
        """
        WITH User
        FOR v, e IN 1..1 ANY CONCAT("User/", @key) Friends
            FILTER NOT e.status
            RETURN {
                key: e._key,
                friend: {
                    key: v._key,
                    username: v.username
                },
                'inbound': e._from == v._id,
                timestamp: e.timestamp
            }
        """,
        bind_vars={'key': key} 
    )

def sendFriendRequest(toKey, fromKey):
    return friendsCollection.insert({
        '_from': 'User/' + fromKey,
        '_to': 'User/' + toKey,
        'gamesPlayed': 0,
        'status': False,
        'timestamp': time.time()
    })

def acceptFriendRequest(friendshipKey):
    return db.aql.execute(
        """
        UPDATE @key WITH { status: True } IN Friends
        """,
        bind_vars={'key': friendshipKey}
    )

def rejectFriendRequest(friendshipKey):
    return db.aql.execute(
        """
        REMOVE @key IN Friends
        """,
        bind_vars={'key': friendshipKey}
    )

def createGame():
    return lobbyCollection.insert({
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
            'theme': "",
            'intendedCompletionTime': 0
        }
    })

def startGame(gameKey, settings):
    # lobbyRes = lobbyCollection.get({
    #     '_key': gameKey
    # });
    # settings = lobbyRes['settings']

    # TRIGGER WEB-SCRAPER
    # destinations = getDestinations(settings)
    result = {
        'destinations': [],
        'trueCompletionTime': 0
    }

    t = time.time()
    return lobbyCollection.update({
        '_key': gameKey,
        'startTime': t,
        'maxTime': t + 24 * 60 * 60,
        'destinations': result['destinations'],
        'trueCompletionTime': result['trueCompletionTime']
    });
    
def updateGameSettings(gameKey):
    t = time.time()
    lobbyRes = lobbyCollection.get({
        '_key': gameKey
    });
    # TRIGGER WEB-SCRAPER
    return lobbyCollection.update({
        'startTime': t,
        'maxTime': t + 24 * 60 * 60,
        'numFinished': 0,
        'members': [],
        'destinations': [],
        
        'radius': 5,
        'busAllowed': True,
        'carAllowed': True,
        'subwayAllowed': True,
        'boatAllowed': True,
        'theme': "",
        'completionTime': 0 
    });