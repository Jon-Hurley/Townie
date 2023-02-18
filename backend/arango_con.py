from arango import ArangoClient
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get('ARANGO_ENDPOINT')
password = os.environ.get('ARANGO_PASSWD')

client = ArangoClient(hosts=[host])
db = client.db('_system', username='root', password=password)

usersSet = db.collection('User')
friendsGraph = db.collection('Friends') 

def createUser(username, password, phoneNumber):
    usersSet.insert({
        'username': username,
        'passwordHash': password,
        'phone': phoneNumber,
        'points': 0,
        'rank': 'beginner',
        'purchases': []
    })

    return

def getUsersBySubstring(substr):
    cursor = db.aql.execute(
        """FOR user IN User
        LET x = CONTAINS(LOWER(user.username), LOWER(@substr), true)
        SORT x
        FILTER x != -1
        LIMIT 10
        RETURN { username: user.username, id: user._key }""",
        bind_vars={'substr': substr}
    )
    return cursor

def getFriendsList(id):
    cursor = db.aql.execute(
        """WITH User
        FOR v, e IN 1..1 ANY @id Friends
        FILTER e.status
        RETURN {
        id: v._id,
        username: v.username""",
        bind_vars={'id': id} 
    )

    return cursor

def sendFriendRequest(toID, fromID):
    friendsGraph.insert({
    '_from': fromID,
    '_to': toID,
    'gamesPlayed': 11001,
    'status': False
    })

    return