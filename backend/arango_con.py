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
gameCollection = db.collection('Games')
playerCollection = db.collection('Players')
destinationCollection = db.collection('Destinations')

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

def createDestination(name, lat, lng):
    try:
        list = [lat, lng]
        return destinationCollection.insert({
            'latitude': lat,
            'longitude': lng,
            'name': name
        })
    except:
        pass

def getNearbyDestinations(lat, lng, radius):
    #technially deprecated
    return destinationCollection.find_in_radius(lat, lng, radius/0.000621371)

#ONLY USED FOR TESTING DESTINATION COLLECTION
def main():
    createDestination("Purdue University", 40.423538, -86.921738)
    list = getNearbyDestinations(40.417912, -86.930481, 1)
    if not list.empty():
        print(list.count())
        first = list.pop()
        print(first)

if __name__ == "__main__":
    main()
