from arango import ArangoClient
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get('ARANGO_ENDPOINT')
password = os.environ.get('ARANGO_PASSWD')

client = ArangoClient(hosts=[host])
db = client.db('_system', username='root', password=password)

userCollection = db.collection('User')
friendsCollection = db.collection('Friends') 

def createUser(username, password, phoneNumber):
    userCollection.insert({
        'username': username,
        'passwordHash': password,
        'phone': phoneNumber,
        'points': 0,
        'rank': 'beginner',
        'purchases': []
    })

    return

def getUsersBySubstring(substr):
    return db.aql.execute(
        """
        FOR user IN User
            LET x = CONTAINS(LOWER(user.username), LOWER(@substr), true)
            SORT x
            FILTER x != -1
            LIMIT 10
            RETURN {
                username: user.username,
                id: user._key
            }
        """,
        bind_vars={'substr': substr}
    )

def getFriendsList(id):
    return db.aql.execute(
        """
        WITH User
        FOR v, e IN 1..1 ANY @id Friends
            FILTER e.status
            RETURN {
                id: v._id,
                username: v.username
            }
        """,
        bind_vars={'id': id} 
    )

def getPendingFriendsList(id):
    return db.aql.execute(
        """
        WITH User
        FOR v, e IN 1..1 ANY @id Friends
            FILTER NOT e.status
            RETURN {
                friendshipKey: e._key,
                friendId: v._id,
                friendUsername: v.username,
                'inbound': e._from == v._id,
                timestamp: e.timestamp
            }
        """,
        bind_vars={'id': id} 
    )

def sendFriendRequest(toID, fromID):
    friendsCollection.insert({
    '_from': fromID,
    '_to': toID,
    'gamesPlayed': 11001,
    'status': False
    })

    return

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