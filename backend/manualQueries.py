import user.queries as queries
import user.views.account as accUtil
import arango_con

usersToCreate = [
    {
        "username": "Arnav",
        "password": "123",
        "phone": "+13176909263"
    },
    {
        "username": "Jacc",
        "password": "123",
        "phone": "+11111111111"
    }
]

friendsToCreate = [
    {
        "_from": 0,
        "_to": 1,
    }
]

for user in usersToCreate:
    username = user['username']
    password = user['password']
    phone = user['phone']
    res = queries.createUser(
        username,
        passwordHash=accUtil.getPasswordHash(password, username),
        phoneNumber=phone
    )
    user['_key'] = res['new']['_key']

for friend in friendsToCreate:
    fromKey = friend['_from']
    toKey = friend['_to']
    res = arango_con.db.aql.execute(
        """
        INSERT {
            _from: CONCAT('User/', @fromKey),
            _to: CONCAT('User/', @toKey),
            gamesPlayed: 0,
            status: true,
            creationTime: DATE_NOW(),
            acceptanceTime: DATE_NOW()
        } IN Friends
        """,
        bind_vars={
            'toKey': usersToCreate[toKey]["_key"],
            'fromKey': usersToCreate[fromKey]["_key"]
        }
    )