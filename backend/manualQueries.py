import user.queries as queries
import user.views.account as accUtil
import arango_con
import datetime

usersToCreate = [
    {
        "username": "Arnav",
        "password": "123",
        "phone": "+13176909263"
    },
    {
        "username": "Jack",
        "password": "123",
        "phone": "+17654121446"
    },
    {
        "username": "Sai",
        "password": "123",
        "phone": "+16309779653"
    },
    {
        "username": "Lexie",
        "password": "123",
        "phone": "+13178288301"
    },
    {
        "username": "Jon",
        "password": "123",
        "phone": "+18124066193"
    }
]

friendsToCreate = [
    {
        "_from": 0,
        "_to": 1,
        "status": True
    },
    {
        "_from": 2,
        "_to": 0,
        "status": True
    },
    {
        "_from": 4,
        "_to": 3,
        "status": True
    },
    {
        "_from": 0,
        "_to": 4,
        "status": True
    }
]

# for user in usersToCreate:
#     username = user['username']
#     password = user['password']
#     phone = user['phone']
#     res = queries.createUser(
#         username,
#         passwordHash=accUtil.getPasswordHash(password, username),
#         phoneNumber=phone
#     )
#     user['_key'] = res['new']['_key']

# for friend in friendsToCreate:
#     fromKey = friend['_from']
#     toKey = friend['_to']
#     res = arango_con.db.aql.execute(
#         """
#         INSERT {
#             _from: CONCAT('User/', @fromKey),
#             _to: CONCAT('User/', @toKey),
#             gamesPlayed: 0,
#             status: @status,
#             creationTime: DATE_NOW(),
#             acceptanceTime: DATE_NOW()
#         } IN Friends
#         """,
#         bind_vars={
#             'toKey': usersToCreate[toKey]["_key"],
#             'fromKey': usersToCreate[fromKey]["_key"],
#             'status': friend['status']
#         }
#     )


t = datetime.datetime.utcnow()
dt = datetime.timedelta(minutes=30)

print(t, dt)