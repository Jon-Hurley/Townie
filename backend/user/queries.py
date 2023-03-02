import arango_con
import time

def createUser(username, password, phoneNumber):
    return arango_con.userCollection.insert({
        'username': username,
        'passwordHash': password,
        'phone': phoneNumber,
        'points': 0,
        'rank': 'beginner',
        'purchases': []
    })

def getUser(userKey, targetKey):
    return arango_con.db.aql.execute(
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
    return arango_con.db.aql.execute(
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
    return arango_con.db.aql.execute(
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
    return arango_con.db.aql.execute(
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
    return arango_con.friendsCollection.insert({
        '_from': 'User/' + fromKey,
        '_to': 'User/' + toKey,
        'gamesPlayed': 0,
        'status': False,
        'timestamp': time.time()
    })

def acceptFriendRequest(friendshipKey):
    return arango_con.db.aql.execute(
        """
        UPDATE @key WITH { status: True } IN Friends
        """,
        bind_vars={'key': friendshipKey}
    )

def rejectFriendRequest(friendshipKey):
    return arango_con.db.aql.execute(
        """
        REMOVE @key IN Friends
        """,
        bind_vars={'key': friendshipKey}
    )