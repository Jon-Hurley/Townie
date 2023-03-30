import arango_con
import time


def createUser(username, passwordHash, phoneNumber):
    return arango_con.userCollection.insert(
        {
            'username': username,
            'passwordHash': passwordHash,
            'phone': phoneNumber,
            'points': 0,
            'rank': 'beginner',
            'purchases': [],
            'login2FA': False,
            'weekly_game_played': False,
            'next_available_game': int(time.time()),
            'hidingState': True
        },
        return_new=True
    )


def getUserByUsername(username):
    return arango_con.userCollection.find({
        'username': username
    })

def updateInfo(userKey, newUsername, newPhone, newPasswordHash,
               newLogin2FA, newHidingState):
    return arango_con.db.aql.execute(
        """
            UPDATE {
                _key: @userKey,
                username: @newUsername,
                phone: @newPhone,
                passwordHash: @newPasswordHash,
                login2FA: @newLogin2FA,
                hidingState: @newHidingState
            } IN User
            RETURN NEW
        """,
        bind_vars={
            'userKey': userKey,
            'newUsername': newUsername,
            'newPhone': newPhone,
            'newPasswordHash': newPasswordHash,
            'newLogin2FA': newLogin2FA,
            'newHidingState': newHidingState
        }
    )

def UpdatePlayableInfo(userKey, weeklyGamePlayed, newTime):
    return arango_con.db.aql.execute(
        """
        FOR user IN User
            FILTER user._key == @userKey
            UPDATE user WITH {
                _key: @userKey,
                weeklyGamePlayed: @weeklyGamePlayed,
                next_available_game: @newTime
            } IN User
            
            RETURN NEW
        """,
        bind_vars={
            'userKey': userKey,
            'weeklyGamePlayed': weeklyGamePlayed,
            'newTime': newTime
        }
    ) 

def updatePassword(userKey, newPasswordHash):
    return arango_con.userCollection.update({
        '_key': userKey,
        'passwordHash': newPasswordHash
    })


def getUserFromPhone(phone):
    return arango_con.db.aql.execute(
        """
            FOR user IN User
            FILTER user.phone == @phone
            RETURN user
        """,
        bind_vars={
            'phone': phone
        }
    )


def deleteUser(userKey, passwordHash):
    return arango_con.db.aql.execute(
        """
        FOR user IN User
            FILTER user._key == @userKey
                && user.passwordHash == @passwordHash

            LET x = (
                FOR v, e IN 1..1 ANY user._id GRAPH Friendships
                    REMOVE e IN Friends
            )
            
            REMOVE user
IN User
RETURN OLD._key
""",
        bind_vars={
            'passwordHash': passwordHash,
            'userKey': str(userKey)
        }
    )


def getUserWithFriendship(userKey, targetKey):
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


def getUser(targetKey):
    return arango_con.db.aql.execute(
        """
FOR user IN User
FILTER user._key == @targetKey
RETURN {
key: user._key,
rank: user.rank,
username: user.username,
points: user.points,
purchases: user.purchases
}
""",
        bind_vars={
            'targetKey': targetKey
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
    return arango_con.db.aql.execute(
        """
        LET originUsername = (
            FOR user IN User
                FILTER user._key == @fromKey
                RETURN user.username
        )[0]

        FOR user IN User
            FILTER user._key == @toKey
            INSERT {
                _from: CONCAT('User/', @fromKey),
                _to: CONCAT('User/', @toKey),
                gamesPlayed: 0,
                status: false,
                creationTime: DATE_NOW()
            } IN Friends
            RETURN {
                key: NEW._key,
                targetPhone: user.phone,
                originUsername
            }
        """,
        bind_vars={
            'toKey': toKey,
            'fromKey': fromKey
        }
    )


def acceptFriendRequest(friendshipKey):
    return arango_con.db.aql.execute(
        """
        LET pp = (
            UPDATE @key
            WITH {
                status: True,
                acceptanceTime: DATE_NOW()
            }
            IN Friends
            RETURN NEW
        )[0]
        LET targetPhone = (
            FOR penis IN User
                FILTER penis._id == pp._from
                RETURN penis.phone
        )[0]
        LET originUsername = (
            FOR penis IN User
                FILTER penis._id == pp._to
                RETURN penis.username
        )[0]
        RETURN {
            targetPhone,
            originUsername
        }
        """,
        bind_vars={'key': friendshipKey}
    )


def rejectFriendRequest(friendshipKey):
    return arango_con.db.aql.execute(
        """
        LET pp = (
            REMOVE @key
            IN Friends
            RETURN OLD
        )[0]
        LET targetPhone = (
            FOR penis IN User
            FILTER penis._id == pp._from
            RETURN penis.phone
        )[0]
        LET originUsername = (
            FOR penis IN User
            FILTER penis._id == pp._to
            RETURN penis.username
        )[0]
        RETURN {
            targetPhone,
            originUsername
        }
        """,
        bind_vars={'key': friendshipKey}
    )

def getRating(theme):
    return arango_con.db.aql.execute(
        """
        FOR theme IN Themes
        FILTER theme.name == @theme
        RETURN {
            name: theme.name,
            rating: theme.rating,
            numRatings: theme.numRatings
        }
        """,
        bind_vars={'theme': theme}
    )

def getGameLog(userKey):
    print(userKey)
    return arango_con.db.aql.execute(
        """
        FOR game IN PastGames
        LET x = POSITION(game.playerKeys, @key, true)
        FILTER x != -1
        RETURN {
            totalDestinations: game.totalDestinations,
            destinationsCompleted: game.destinationsCompleted,
            timeSpent: game.timeSpent,
            points: game.points
        }
        """,
        bind_vars={'key': int(userKey)}
    )