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
    userCollection = db.collection('User')
    userCollection.add_hash_index(
        fields=['username'],
        unique=True
    )
    userCollection.add_persistent_index(
        fields=['phone'],
        unique=True
    )

if not db.has_collection('Games'):
    db.create_collection('Games')
    gameCollection = db.collection('Games')

if not db.has_collection('Purchasables'):
    db.create_collection('Purchasables')
    purchasablesCollection = db.collection('Purchasables')

if not db.has_collection('Destinations'):
    db.create_collection('Destinations')
    destinationCollection = db.collection('Destinations')
    destinationCollection.add_geo_index(
        fields=['lon', 'lat']
    )
    destinationCollection.add_persistent_index(
        fields=['name'],
        unique=True
    )

if not db.has_collection('Purchases'):
    db.create_collection('Purchases', edge=True)
    purchaseCollection = db.collection('Purchases')
    purchaseCollection.add_persistent_index(
        fields=['_from', '_to'],
        unique=True
    )

if not db.has_collection('Friends'):
    db.create_collection('Friends', edge=True)
    friendsCollection = db.collection('Friends')

if not db.has_collection('Players'):
    db.create_collection('Players', edge=True)
    playerCollection = db.collection('Players')
    playerCollection.add_hash_index(
        fields=['connectionId'],
        unique=True,
        sparse=True,
        name='connectionIdToPlayer',
        in_background=True
    )

if not db.has_collection('Itineraries'):
    db.create_collection('Itineraries', edge=True)
    itineraryCollection = db.collection('Itineraries')

if not db.has_collection('Themes'):
    db.create_collection('Themes')
    themeCollection = db.collection('Themes')

if not db.has_collection('UnusedItineraries'):
    db.create_collection('UnusedItineraries', edge=True)
    unusedItineraryCollection = db.collection('UnusedItineraries')
    unusedItineraryCollection.add_persistent_index(
        fields=['_from', 'index'],
        unique=True,
        sparse=True
    )

if not db.has_graph('Consumerships'):
    consumershipGraph = db.create_graph('Consumerships')
    consumershipGraph.create_edge_definition(
        edge_collection='Purchases',
        from_vertex_collections=['User'],
        to_vertex_collections=['Purchasables']
    )

if not db.has_graph('Friendships'):
    friendshipGraph = db.create_graph('Friendships')
    friendshipGraph.create_edge_definition(
        edge_collection='Friends',
        from_vertex_collections=['User'],
        to_vertex_collections=['User']
    )

if not db.has_graph('Playerships'):
    playershipGraph = db.create_graph('Playerships')
    playershipGraph.create_edge_definition(
        edge_collection='Players',
        from_vertex_collections=['User'],
        to_vertex_collections=['Games']
    )

userCollection = db.collection('User')
friendsCollection = db.collection('Friends')
gameCollection = db.collection('Games')
playerCollection = db.collection('Players')
destinationCollection = db.collection('Destinations')
itineraryCollection = db.collection('Itineraries')
unusedItineraryCollection = db.collection('UnusedItineraries')
purchasablesCollection = db.collection('Purchasables')
purchaseCollection = db.collection('Purchases')