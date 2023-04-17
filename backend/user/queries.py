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
            'weeklyGamePlayed': False,
            'nextAvailableGame': 0,
            'hidingState': False,
            'isPremium': False
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
                nextAvailableGame: @newTime
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

def activatePremium(userKey, customerId, subscriptionId):
    return arango_con.userCollection.update({
        '_key': userKey,
        'isPremium': True,
        'stripeCustomerId': customerId,
        'stripeSubscriptionId': subscriptionId,
        'premiumActivationTime': int(time.time() * 1000)
    }, return_new=True)

def updatePremium(customerId, isPremium, subscriptionId):
    return arango_con.db.aql.execute(
        """
        FOR user IN User
            FILTER user.stripeCustomerId == @customerId
               AND user.stripeCustomerId != null
            UPDATE user
            WITH {
                isPremium: @isPremium,
                stripeSubscriptionId: @subscriptionId
            }
            IN User
            RETURN NEW
        """,
        bind_vars={
            'customerId': customerId,
            'isPremium': isPremium,
            'subscriptionId': subscriptionId
        }
    )

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

def getUserInternal(userKey):
    return arango_con.userCollection.find({
        '_key': userKey
    })


def getUserFromPhoneOrUsername(phone, username):
    return arango_con.db.aql.execute(
        """
        FOR user IN User
        FILTER user.phone == @phone || 
        user.username == @username
        RETURN user
        """,
        bind_vars={
            'phone': phone,
            'username': username
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
            FOR v, e IN 1..1 ANY userId GRAPH Friendships
                FILTER v._key == @targetKey
                RETURN {
                    status: e.status,
                    'inbound': e._to == userId,
                    key: e._key
                }
        )[0]

        LET mutualFriends = COUNT(
            FOR v, e, p IN 2..2 ANY
                CONCAT("User/", @userKey)
                GRAPH Friendships
                PRUNE e.status == false

                FILTER v._key == @targetKey
                RETURN p.vertices[1]
        )

        LET networkDistance = (
            FOR v, e, p IN 1..4 ANY
                CONCAT("User/", @userKey)
                GRAPH Friendships
                PRUNE e.status == false
                OPTIONS { order: "bfs" }
                
                FILTER v._key == @targetKey
                LIMIT 1
                RETURN COUNT(p.edges)
        )[0] || 5

        FOR user IN User
            FILTER user._key == @targetKey
            RETURN {
                key: user._key,
                rank: user.rank,
                username: user.username,
                points: user.points,
                isPremium: user.isPremium,
                purchases: user.purchases,
                friendship: f,
                mutualFriends,
                networkDistance
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
                purchases: user.purchases,
                isPremium: user.isPremium
            }
        """,
        bind_vars={
            'targetKey': targetKey
        }
    )


def getUsersBySubstring(substr, userKey):
    return arango_con.db.aql.execute(
        """
        LET lowerSubstr = LOWER(@substr)

        LET userFriends = (
            FOR v IN 1..1 ANY CONCAT("User/", @userKey) GRAPH Friendships
                RETURN v._key
        )

        LET mutualFriendCounts = (
            FOR v, e, p IN 2..2 ANY
                CONCAT("User/", @userKey)
                GRAPH Friendships
                PRUNE e.status == false
                
                LET target = p.vertices[2]
                COLLECT user = target WITH COUNT INTO mutualFriends
                RETURN {
                    key: user._key,
                    mutualFriends
                }
        )

        LET searchRes = (
            FOR user in User
                LET lowerUsername = LOWER(user.username)
                LET starts = STARTS_WITH(lowerUsername, lowerSubstr)
                LET dist = LEVENSHTEIN_DISTANCE(lowerUsername, lowerSubstr)
                FILTER starts || dist <= LENGTH(lowerSubstr) * 0.5
                SORT starts DESC, dist ASC
                LIMIT 10
                RETURN {
                    key: user._key,
                    username: user.username,
                    isPremium: user.isPremium,
                    dist
                }
        )

        FOR user1 IN searchRes
            LET mutualFriends = (
                For user2 IN mutualFriendCounts
                    FILTER user1.key == user2.key
                    RETURN user2.mutualFriends
            )[0] || 0
            
            LET isFriend = (
                FOR v, e IN 1..1 ANY CONCAT("User/", @userKey) GRAPH Friendships
                    FILTER v._key == user1.key
                    RETURN e.status
            )[0] || false

            LET targetFriends = (
                FOR v IN 1..1 ANY user1 GRAPH Friendships
                    RETURN v._key
            )

            LET unionLength = LENGTH(UNION_DISTINCT(userFriends, targetFriends))
            LET jaccardIndex = unionLength == 0 ? 0 : mutualFriends / unionLength

            RETURN {
                key: user1.key,
                username: user1.username,
                isPremium: user1.isPremium,
                mutualFriends,
                isFriend,
                jaccardIndex
            }
        """,
        bind_vars={
            'substr': substr,
            'userKey': userKey     
        }
    )

def getOnlySuggestedUsers(userKey):
    return arango_con.db.aql.execute(
        """
        LET userFriends = (
            FOR v IN 1..1 ANY CONCAT("User/", @userKey) GRAPH Friendships
                RETURN v._key
        )
        
        LET mutualFriendCounts = (
            FOR v, e, p IN 2..2 ANY
                CONCAT("User/", @userKey)
                GRAPH Friendships
                PRUNE e.status == false
                
                LET target = p.vertices[2]
                COLLECT user = target WITH COUNT INTO mutualFriends
                RETURN {
                    user,
                    mutualFriends
                }
        )

        FOR mf IN mutualFriendCounts
            LET user = mf.user
            LET mutualFriends = mf.mutualFriends

            LET isFriend = (
                FOR v, e IN 1..1 ANY CONCAT("User/", @userKey) GRAPH Friendships
                    FILTER v._key == user._key
                    RETURN e.status
            )[0] || false
            FILTER isFriend == false

            LET targetFriends = (
                FOR v, e IN 1..1 ANY user GRAPH Friendships
                    FILTER e.status
                    RETURN v._key
            )
            LET unionLength = LENGTH(UNION_DISTINCT(userFriends, targetFriends))
            LET jaccardIndex = mutualFriends / unionLength
            FILTER jaccardIndex >= 0.25
            SORT jaccardIndex DESC
            LIMIT 10
            
            RETURN {
                key: user._key,
                username: user.username,
                isPremium: user.isPremium,
                mutualFriends,
                isFriend,
                jaccardIndex
            }
        """,
        bind_vars={
            'userKey': userKey     
        }
    )


def getFriendsList(key):
    return arango_con.db.aql.execute(
        """
        FOR v, e IN 1..1 ANY CONCAT("User/", @key) GRAPH Friendships
            FILTER e.status
            RETURN {
                key: v._key,
                username: v.username,
                isPremium: v.isPremium
            }
        """,
        bind_vars={'key': key}
    )

def getUsersInGame(userKey):
    return arango_con.db.aql.execute(
        """
        LET userId = CONCAT("User/", @userKey)

        LET friends = (
            FOR friend, e IN 1..1 ANY userId GRAPH Friendships
                FILTER e.status
                RETURN friend
        )

        LET onlineFriends = (
            FOR friend in friends
                LET isOnline = (
                    FOR v, e IN 1..1 ANY friend._id GRAPH Playerships
                        FILTER e.connectionId != NULL
                        FILTER v != NULL
                        RETURN v._key
                )
                FILTER LENGTH(isOnline) != 0
                
                RETURN {
                    username: friend.username,
                    key: friend._key,
                    isPremium: friend.isPremium,
                    gameKey: isOnline[0]
                }
        )

        LET prevPlayers = (
            FOR playerUser IN 2..2 ANY userId GRAPH Playerships
                RETURN DISTINCT playerUser
        )

        LET onlinePrevPlayers = (
            FOR playerUser IN prevPlayers
                LET isFriend = LENGTH(
                    FOR f in friends
                        FILTER f._key == playerUser._key
                        RETURN f
                ) != 0
                FILTER !isFriend
                
                LET isOnline = (
                    FOR v, e IN 1..1 ANY playerUser._id GRAPH Playerships
                        FILTER e.connectionId != NULL
                        FILTER v != NULL
                        RETURN v._key
                )
                FILTER LENGTH(isOnline) != 0
                
                RETURN {
                    username: playerUser.username,
                    key: playerUser._key,
                    isPremium: playerUser.isPremium,
                    gameKey: NULL
                }
        )

        RETURN APPEND(onlinePrevPlayers, onlineFriends)
        """,
        bind_vars={'userKey': userKey}
    )


def getPendingFriendsList(key):
    return arango_con.db.aql.execute(
        """
        FOR v, e IN 1..1 ANY CONCAT("User/", @key) GRAPH Friendships
            FILTER NOT e.status
            RETURN {
                key: e._key,
                friend: {
                    key: v._key,
                    username: v.username,
                    isPremium: v.isPremium
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
        SORT NGRAM_SIMILARITY(theme.name, @theme, 1) DESC
        LIMIT 1
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
        FOR v, e
        IN 1..1
        ANY CONCAT("User/", @key)
        GRAPH Playerships
            RETURN {
                game: v,
                player: e
            }
        """,
        bind_vars={'key': int(userKey)}
    )


def submitRating(theme, rating, numRatings):
    return arango_con.db.aql.execute(
        """
        LET x = (
            FOR theme IN Themes
            FILTER theme.name == @theme
            UPDATE theme._key WITH {
                rating: @rating,
                numRatings: @numRatings
            } IN Themes
            RETURN NEW
        )[0]
        RETURN {
            name: x.name,
            rating: x.rating,
            numRatings: x.numRatings
        }
        """,
        bind_vars={'theme': theme, 'rating': rating, 'numRatings': numRatings}
    )
