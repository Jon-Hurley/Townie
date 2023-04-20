import boto3
import os
import asyncio
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

async def propogateToPlayers(data, conExclusion={}):
    print("DATA", data)
    players = data['players']

    for player in players:
        connectionId = player['connectionId']
        if connectionId in conExclusion:
            continue

        data['player'] = player # add player's own data to their game data
        try:
            data['nextDestination'] = data['destinations'][player['destinationIndex']]
        except:
            data['nextDestination'] = None
        
        asyncio.create_task(
            propogateToUser(
                connectionId,
                data = json.dumps({
                    'method': 'update-game',
                    'data': data,
                })
            )
        )

async def propogateToUsers(connectionIds, data):
    for connectionId in connectionIds:
        asyncio.create_task(
            propogateToUser(connectionId, data)
        )

async def propogateToUser(connectionId, data):
    try:
        client.post_to_connection(
            Data=data,
            ConnectionId=connectionId
        )
    except Exception as err:
        print("PROPOGATE ERROR:", connectionId)

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