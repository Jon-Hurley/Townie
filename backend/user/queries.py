import arango_con
import time


def createUser(username, passwordHash, phoneNumber):
    return arango_con.userCollection.insert(
        {
            'username': username,
            'passwordHash': passwordHash,
            'phone': phoneNumber,
            'points': 0,
            'cumPoints': 0,
            'rank': 'beginner',
            'login2FA': False,
            'weeklyGamePlayed': False,
            'nextAvailableGame': 0,
            'hidingState': False,
            'isPremium': False
        },
        return_new=True
    )


def getUserByUsername(username):
    return arango_con.db.aql.execute(
        """
        FOR user IN User
            FILTER user.username == @username
            LET purchases = (
                FOR v, e IN 1..1 ANY user._id GRAPH Consumerships
                    SORT v.category ASC, e.purchaseTime DESC
                    RETURN MERGE(v, { isActive: e.isActive })
            )
            RETURN MERGE(user, { purchases })
        """,
        bind_vars={
            'username': username
        }
    )

def getUserFromPhone(phone):
    return arango_con.db.aql.execute(
        """
        FOR user IN User
            FILTER user.phone == @phone
            LET purchases = (
                FOR v, e IN 1..1 ANY user._id GRAPH Consumerships
                    SORT v.category ASC, e.purchaseTime DESC
                    RETURN MERGE(v, { isActive: e.isActive })
            )
            RETURN MERGE(user, { purchases })
        """,
        bind_vars={
            'phone': phone
        }
    )

def getUserFromPhoneOrUsername(phone, username):
    return arango_con.db.aql.execute(
        """
        FOR user IN User
            FILTER user.phone == @phone
                || user.username == @username
            RETURN user._key
        """,
        bind_vars={
            'phone': phone,
            'username': username
        }
    )

def updateInfo(userKey, newUsername, newPhone, newPasswordHash,
               newLogin2FA, newHidingState):
    return arango_con.db.aql.execute(
        """
            LET purchases = (
                FOR v, e IN 1..1 ANY
                CONCAT("User/", @userKey)
                GRAPH Consumerships
                    SORT v.category ASC, e.purchaseTime DESC
                    RETURN MERGE(v, { isActive: e.isActive })
            )
            
            UPDATE {
                _key: @userKey,
                username: @newUsername,
                phone: @newPhone,
                passwordHash: @newPasswordHash,
                login2FA: @newLogin2FA,
                hidingState: @newHidingState
            } IN User
            RETURN MERGE(NEW, { purchases })
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
        LET purchases = (
            FOR v, e IN 1..1 ANY
            CONCAT("User/", @userKey)
            GRAPH Consumerships
                SORT v.category ASC, e.purchaseTime DESC
                RETURN MERGE(v, { isActive: e.isActive })
        )

        FOR user IN User
            FILTER user._key == @userKey
            UPDATE user WITH {
                _key: @userKey,
                weeklyGamePlayed: @weeklyGamePlayed,
                nextAvailableGame: @newTime
            } IN User
            
            RETURN MERGE(NEW, { purchases })
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

        LET purchases = (
            FOR v, e IN 1..1 ANY userId GRAPH Consumerships
                SORT v.category ASC, e.purchaseTime DESC
                RETURN MERGE(v, { isActive: e.isActive })
        )

        FOR user IN User
            FILTER user._key == @targetKey
            RETURN {
                key: user._key,
                rank: user.rank,
                username: user.username,
                cumPoints: user.cumPoints,
                isPremium: user.isPremium,
                purchases,
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

            LET purchases = (
                FOR v, e IN 1..1 ANY user._id GRAPH Consumerships
                    SORT v.category ASC, e.purchaseTime DESC
                    RETURN MERGE(v, { isActive: e.isActive })
            )

            RETURN {
                key: user._key,
                rank: user.rank,
                username: user.username,
                points: user.points,
                purchases: purchases,
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


def getGameLog(targetKey):
    return arango_con.db.aql.execute(
        """
        FOR v, e IN 1..1 ANY
        CONCAT("User/", @targetKey)
        GRAPH Playerships
            LET theme = (
                FOR theme in Themes
                    SORT NGRAM_SIMILARITY(theme.name, v.settings.theme, 1) DESC
                    LIMIT 1
                    RETURN theme
            )[0]

            RETURN {
                game: v,
                player: e,
                theme
            }
        """,
        bind_vars={
            'targetKey': str(targetKey)
        }
    )


def getSummary(gameKey, userKey):
    return arango_con.db.aql.execute(
        """
        WITH User, Destinations

        LET destinations = (
            FOR v, e IN 1..1 OUTBOUND CONCAT("Games/", @gameKey) Itineraries
                RETURN {
                    index: e.index,
                    points: e.points,
                    name: v.name,
                    lon: v.longitude,
                    lat: v.latitude,
                    timeToCompletion: e.timeToCompletion
                }
        )

        LET players = (
            FOR v, e IN 1..1 INBOUND CONCAT("Games/", @gameKey) Players
                FILTER v != null
                RETURN {
                    key: v._key,
                    username: v.username,
                    isPremium: v.isPremium,
                    destinationIndex: e.destinationIndex,
                    points: e.points,
                    totalDistance: e.totalDistance,
                    totalTime: e.totalTime,
                    isFinished: e.destinationIndex == LENGTH(destinations)
                }
        )

        LET numFinished = LENGTH(
            FOR p IN Players
                FILTER p.isFinished
                RETURN p
        )

        FOR game IN Games
            FILTER game._key == @gameKey
            LET theme = (
                FOR theme in Themes
                    SORT NGRAM_SIMILARITY(theme.name, game.settings.theme, 1) DESC
                    LIMIT 1
                    RETURN theme
            )[0]

            LET userRating = (
                FOR r IN ThemeRatings
                    FILTER r._from == CONCAT("User/", @userKey)
                        && r._to == theme._id
                    RETURN {
                        rating: r.rating,
                        lastUpdated: r.lastUpdated
                    }
            )[0]
            
            RETURN {
                game,
                players,
                destinations,
                theme,
                numFinished,
                userRating
            }
    """,
        bind_vars={
            'gameKey': str(gameKey),
            'userKey': str(userKey)
        }
    )

def getDestination(destKey, userKey):
    return arango_con.db.aql.execute(
        """
        WITH User, Destinations

        FOR dest IN Destinations
            FILTER dest._key == @destKey

            LET theme = (
                FOR theme in Themes
                    SORT NGRAM_SIMILARITY(theme.name, dest.theme, 1) DESC
                    LIMIT 1
                    RETURN theme
            )[0]

            LET userRating = (
                FOR r IN DestinationRatings
                    FILTER r._from == CONCAT("User/", @userKey)
                        && r._to == dest._id
                    RETURN {
                        rating: r.rating,
                        lastUpdated: r.lastUpdated
                    }
            )[0]
            
            RETURN {
                destination: dest,
                theme,
                userRating
            }
        """,
        bind_vars={
            'destKey': str(destKey),
            'userKey': str(userKey)
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


def submitThemeRating(userKey, themeKey, newRating):
    return arango_con.db.aql.execute(
        """
        LET res = (
            UPSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Themes/", @themeKey)
            }
            INSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Themes/", @themeKey),
                rating: @newRating,
                lastUpdated: DATE_NOW()
            }
            UPDATE {
                rating: @newRating,
                lastUpdated: DATE_NOW()
            }
            IN ThemeRatings
            RETURN OLD
        )[0]

        LET ratingAdded = res == null ? 1 : 0
        LET ratingDelta = ratingAdded ? @newRating : @newRating - res.rating

        FOR theme IN Themes
            FILTER theme._key == @themeKey

            LET prevRatingPoints = theme.ratingPoints ? theme.ratingPoints : 0
            LET prevNumRatings = theme.numRatings ? theme.numRatings : 0

            UPDATE theme
            WITH {
                ratingPoints: prevRatingPoints + ratingDelta,
                numRatings: prevNumRatings + ratingAdded
            }
            IN Themes
            RETURN {
                ratingAdded,
                ratingDelta
            }
        """,
        bind_vars={
            'userKey': userKey,
            'themeKey': themeKey,
            'newRating': newRating
        }
    )

def submitDestRating(userKey, destKey, newRating):
    return arango_con.db.aql.execute(
        """
        LET res = (
            UPSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Destinations/", @destKey)
            }
            INSERT {
                _from: CONCAT("User/", @userKey),
                _to: CONCAT("Destinations/", @destKey),
                rating: @newRating,
                lastUpdated: DATE_NOW()
            }
            UPDATE {
                rating: @newRating,
                lastUpdated: DATE_NOW()
            }
            IN DestinationRatings
            RETURN OLD
        )[0]

        LET ratingAdded = res == null ? 1 : 0
        LET ratingDelta = ratingAdded ? @newRating : @newRating - res.rating

        FOR dest IN Destinations
            FILTER dest._key == @destKey

            LET prevRatingPoints = dest.ratingPoints ? dest.ratingPoints : 0
            LET prevNumRatings = dest.numRatings ? dest.numRatings : 0
            
            UPDATE dest
            WITH {
                ratingPoints: prevRatingPoints + ratingDelta,
                numRatings: prevNumRatings + ratingAdded
            }
            IN Destinations
            RETURN {
                ratingAdded,
                ratingDelta
            }
        """,
        bind_vars={
            'userKey': userKey,
            'destKey': destKey,
            'newRating': newRating
        }
    )


def getPurchasables(userKey):
    return arango_con.db.aql.execute(
        """
        LET user = (
            FOR user IN User
                FILTER user._key == @userKey
                RETURN user
        )
        LET purchased = (
            FOR v, e IN 1..1 ANY
            CONCAT("User/", @userKey)
            GRAPH Consumerships
                RETURN v
        )
        FOR p IN Purchasables
            LET matches = (
                FOR x IN purchased
                    FILTER p._id == x._id
                    RETURN x
            )
            FILTER LENGTH(matches) == 0
            SORT p.isPremium ASC, p.cost ASC
            RETURN p
        """,
        bind_vars={
            'userKey': userKey
        }
    )

def makePurchase(userKey, purchasableKey):
    return arango_con.db.aql.execute(
        """
        LET user = (
            FOR user IN User
                FILTER user._key == @userKey
                RETURN user
        )[0]

        LET matches = (
            FOR p IN Purchasables
                FILTER p._key == @purchasableKey
                RETURN p
        )

        LET res = (
            For p in matches
                FILTER !p.isPremium
                    OR user.isPremium
                FILTER p.cost <= user.points
                
                LET userRes = (
                    UPDATE user
                    WITH {
                        points: user.points - p.cost
                    }
                    IN User
                )

                INSERT {
                    _from: CONCAT("User/", @userKey),
                    _to: p._id,
                    purchaseTime: DATE_NOW(),
                    isActive: false
                }
                INTO Purchases
                RETURN NEW
        )[0]

        LET item = matches[0]
        RETURN {
            foundItem: item != null,
            hasPremiumReq: !item.isPremium OR user.isPremium,
            enoughPoints: user.points - item.cost,
            alreadyPurchased: res == null
        }
        """,
        bind_vars={
            'userKey': userKey,
            'purchasableKey': purchasableKey
        }
    )

def activatePurchase(userKey, purchasableKey):
    return arango_con.db.aql.execute(
        """
        LET user = (
            FOR user IN User
                FILTER user._key == @userKey
                RETURN user
        )[0]

        LET purchase = (
            FOR p IN Purchasables
                FILTER p._key == @purchasableKey
                return p
        )[0]

        FOR v, e IN 1..1 ANY user._id GRAPH Consumerships
            FILTER purchase.category == v.category
            UPDATE e._key WITH {
                isActive: @purchasableKey == v._key ? !e.isActive : false
            }
            IN Purchases
            RETURN NEW
        """,
        bind_vars={
            'userKey': userKey,
            'purchasableKey': purchasableKey
        }
    )