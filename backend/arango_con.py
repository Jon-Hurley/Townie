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

def createUser(username, password, phoneNumber):
    return userCollection.insert({
        'username': username,
        'passwordHash': password,
        'phone': phoneNumber,
        'points': 0,
        'rank': 'beginner',
        'purchases': []
    })

def login(username, password):
    return db.aql.execute(
        """
        LET temp = TRUE
        FOR user IN User
            FILTER LOWER(user.username) == LOWER(@username)
            IF(user.passwordHash == @password) {
                temp = FALSE
                RETURN {
                    success: true,
                    key: user._key,
                    username: user.username,
                    phoneNumber: user.phone,
                    points: user.points,
                    rank: user.ranks,
                    purchases: user.purchases
                }
            }
        END
        IF (temp)
            THEN RETURN { success: false }
        """,
        bind_vars={
            'username': username,
            'password': password
        }
    )

def updateInfo(userKey, newUser, newPhone):
    return db.aql.execute(
        """
        LET result = (
            FOR user IN User
                FILTER user._key == (@userKey)
                UPDATE user WITH MERGE(user, { username: (@newUser), phone: (@newPhone) }) IN User
                RETURN {
                    success: true,
                    key: user._key,
                    username: user.username,
                    phoneNumber: user.phone,
                    points: user.points,
                    rank: user.ranks,
                    purchases: user.purchases
                }
        )
        IF LENGTH(result) == 0
            RETURN { success: false }
        ELSE
            RETURN result
        END
        """,
        bind_vars={
            'userKey': userKey,
            'newUser': newUser,
            'newPhone': newPhone
        }
    )

def deleteUser(userKey):
    return db.aql.execute(
        """
        LET result = REMOVE @key IN User

        IF result.deleted == 0
            RETURN { success: false }
        ELSE
            RETURN { success: true }
        END 
        """,
        bind_vars={'key': userKey}
    )
       

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