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

query = "FOR user IN User FILTER CONTAINS(LOWER(user.username), LOWER(@substr)) RETURN { user }"

cursor = db.aql.execute(
    query, bind_vars={'substr': 'arnav'}
)

print(cursor.batch())

# print(res)