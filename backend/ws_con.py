import boto3
import os
from dotenv import load_dotenv
import json

load_dotenv()

WS_API = os.environ.get('WS_ENDPOINT')

client = boto3.client(
    'apigatewaymanagementapi',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    endpoint_url=os.environ.get('WS_ENDPOINT'),
)

# PROPOGATE CHANGES BACK TO USERS VIA WS API
# FUCK DJANGO AND ITS BS CONCURRENCY REQS.

def propogateUpdates(users, data, conExcl={}):
    data = json.dumps(data)
    for user in users:
        connectionId = user['connectionId']
        if connectionId in conExcl:
            continue
        propogateUpdate(connectionId, data)
    return True

def propogateUpdate(connectionId, data):
    try:
        print(connectionId, data)
        response = client.post_to_connection(
            Data=data,
            ConnectionId=connectionId
        )
        return response
    except Exception as err:
        print(err)
        return None

def forceDisconnect(connectionId):
    try:
        print("DISCONNECTING:", connectionId)
        response = client.delete_connection(
            ConnectionId=connectionId
        )
        return response
    except Exception as err:
        print(err)
        return None