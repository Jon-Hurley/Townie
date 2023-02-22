from arango import ArangoClient
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get('ARANGO_ENDPOINT')
password = os.environ.get('ARANGO_PASSWD')

client = ArangoClient(hosts=[host])
db = client.db('_system', username='root', password=password)

userCollection = db.collection('User')
friendsCollection = db.collection('Friends')
gameCollection = db.collection('Games')
playerCollection = db.collection('Players')