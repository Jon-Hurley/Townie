from arango import ArangoClient
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get('ARANGO_ENDPOINT')
password = os.environ.get('ARANGO_PASSWD')

client = ArangoClient(hosts=[host])
db = client.db('_system', username='root', password=password)

users = db.collection('User')
res = users.insert({
  'username': 'Arnav',
  'passwordHash': 'password',
  'phone': '+13176909263',
  'points': 50,
  'rank': 'explorer',
  'purchases': []
})

print(res)