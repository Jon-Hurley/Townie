from arango import ArangoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the ArangoDB client.
client = ArangoClient(hosts=os.environ.get('ARANGO_ENDPOINT'))

# Connect to "_system" database as root user.
# This returns an API wrapper for "_system" database.
sys_db = client.db('_system', username='root', password=os.environ.get('ARANGO_PASSWD'))

print(sys_db)