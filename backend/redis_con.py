import redis
import os
from dotenv import load_dotenv

load_dotenv()

r = redis.StrictRedis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    username=os.environ.get('REDIS_USERNAME'),
    password=os.environ.get('REDIS_PASSWORD'),
    charset="utf-8",
    decode_responses=True
);

def savePaymentSession(userKey, sessionId):
    r.set(sessionId, userKey)
    r.set(userKey, sessionId)

def getSessionUser(sessionId):
    return r.get(sessionId)

def getUserSession(userKey):
    return r.get(userKey)

def deletePaymentSession(sessionId):
    userKey = r.get(sessionId)
    r.delete(sessionId)
    r.delete(userKey)

def deletePaymentSessionViaUser(userKey):
    sessionKey = r.get(userKey)
    r.delete(sessionKey)
    r.delete(userKey)

# def createConnectionCredentials(userKey, gameKey):
#     password = r.acl_genpass()
#     r.acl_deluser(userKey)
#     r.acl_setuser(
#         username=userKey,
#         passwords=[password],
#         commands=[
#             '-@all',
#             '+subscribe|' + gameKey,
#             '+publish|' + gameKey
#         ]
#     )
#     return password