import redis
import os
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    username=os.environ.get('REDIS_USERNAME'),
    password=os.environ.get('REDIS_PASSWORD')
);

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