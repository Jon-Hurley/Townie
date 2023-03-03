from arango import ArangoClient, DocumentInsertError
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get('ARANGO_ENDPOINT')
password = os.environ.get('ARANGO_PASSWD')

client = ArangoClient(hosts=[host])
db = client.db('_system', username='root', password=password)

if not db.has_collection('User'):
    db.create_collection('User')
    db.create_collection('Games')
    db.create_collection('Destinations')

    db.create_collection('Friends', edge=True)
    db.create_collection('Players', edge=True)
    db.create_collection('Itineraries', edge=True)

    userCollection = db.collection('User')
    friendsCollection = db.collection('Friends')
    gameCollection = db.collection('Games')
    playerCollection = db.collection('Players')
    destinationCollection = db.collection('Destinations')
    itineraryCollection = db.collection('Itineraries')

    userCollection.add_persistent_index(
        fields=['username'],
        unique=True,
        sparse=True
    )
    userCollection.add_persistent_index(
        fields=['phone'],
        unique=True,
        sparse=True
    )

    destinationCollection.add_geo_index(
        fields=['lon', 'lat']
    )
    destinationCollection.add_persistent_index(
        fields=['name'],
        unique=True,
        sparse=True
    )

    friendsCollection.add_persistent_index(
        fields=['_from', '_to'],
        unique=True,
        sparse=True
    )
    
    playerCollection.add_persistent_index(
        fields=['_from'],
        unique=True,
        sparse=True
    )
    playerCollection.add_persistent_index(
        fields=['connectionId'],
        unique=True,
        sparse=True
    )

    itineraryCollection.add_persistent_index(
        fields=['_from', 'index'],
        unique=True,
        sparse=True
    )
    itineraryCollection.add_persistent_index(
        fields=['_from', '_to'],
        unique=True,
        sparse=True
    )

userCollection = db.collection('User')
friendsCollection = db.collection('Friends')
gameCollection = db.collection('Games')
playerCollection = db.collection('Players')
destinationCollection = db.collection('Destinations')
itineraryCollection = db.collection('Itineraries')