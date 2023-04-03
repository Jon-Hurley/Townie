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
    db.create_collection('UnusedItineraries', edge=True)

    userCollection = db.collection('User')
    friendsCollection = db.collection('Friends')
    gameCollection = db.collection('Games')
    playerCollection = db.collection('Players')
    destinationCollection = db.collection('Destinations')
    itineraryCollection = db.collection('Itineraries')
    unusedItineraryCollection = db.collection('UnusedItineraries')

    userCollection.add_hash_index(
        fields=['username'],
        unique=True
    )
    userCollection.add_persistent_index(
        fields=['phone'],
        unique=True
    )

    destinationCollection.add_geo_index(
        fields=['lon', 'lat']
    )
    destinationCollection.add_persistent_index(
        fields=['name'],
        unique=True
    )

    playerCollection.add_hash_index(
        fields=['connectionId'],
        unique=True,
        sparse=True,
        name='connectionIdToPlayer',
        in_background=True
    )

    db.create_graph(
        'Friendships',
        edge_definitions={
            'edge_collection': 'Friends',
            'from_vertex_collections': ['User'],
            'to_vertex_collections': ['User']
        },
        shard_count=1,
        replication_factor=3,
        write_concern=3
    )
    db.create_graph(
        'Playerships',
        edge_definitions={
            'edge_collection': 'Players',
            'from_vertex_collections': ['User'],
            'to_vertex_collections': ['Games']
        },
        shard_count=1,
        replication_factor=3,
        write_concern=3
    )
    unusedItineraryCollection.add_persistent_index(
        fields=['_from', 'index'],
        unique=True,
        sparse=True
    )
    unusedItineraryCollection.add_persistent_index(
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
unusedItineraryCollection = db.collection('UnusedItineraries')