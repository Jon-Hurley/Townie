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

# PROPOGATE CHANGES BACK TO USERS VIA AWS WS API

def propogateUpdates(data, conExcl={}):
    players = data['players']
    for player in players:
        connectionId = player['connectionId']
        if connectionId not in conExcl:
            propogateUpdate(connectionId, player, data=data)
    return True

def propogateUpdate(connectionId, player, data):
    data['player'] = player
    data = json.dumps({
        'method': 'update-game',
        'data': data,
    })

    try:
        print("Emitting to: ", connectionId)
        response = client.post_to_connection(
            Data=data,
            ConnectionId=connectionId
        )
        return response
    except Exception as err:
        print(err)
        return None

def propogateNewMessage(messageObj, connectionIds):
    data = json.dumps({
        'method': 'new-message',
        'data': messageObj
    })
    for connectionId in connectionIds:
        try:
            client.post_to_connection(
                Data=data,
                ConnectionId=connectionId
            )
        except Exception as err:
            print(err)

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