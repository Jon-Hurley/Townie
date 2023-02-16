from arango import ArangoClient
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get('ARANGO_ENDPOINT')
password = os.environ.get('ARANGO_PASSWD')

client = ArangoClient(hosts=[host])
db = client.db('_system', username='root', password=password)

users = db.collection('User')
# res = users.insert({
#   'username': 'Jon',
#   'passwordHash': 'password123',
#   'phone': '+11234567890',
#   'points': 1250,
#   'rank': 'spaceman',
#   'purchases': []
# })

getUsersBySubstring = "FOR user IN User FILTER CONTAINS(LOWER(user.username), LOWER(@substr)) RETURN { username: user.username, id: user._key }"

getUserWithID = "FOR user IN User FILTER user._key == '10907' RETURN { user }"

cursor = db.aql.execute(
    getUsersBySubstring, bind_vars={'substr': 'arnav'}
)

cursor2 = db.aql.execute(
    getUserWithID
)

print("Printing substrings test!")
print(cursor.batch())

print("Printing user id test!")
print(cursor2.batch())

# print(res)