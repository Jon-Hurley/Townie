from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import requests
import os
load_dotenv()

# BACKEND_URL = os.environ.get('BACKEND_URL')
BACKEND_URL = 'http://127.0.0.1:8000/'

class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, websocket: WebSocket, gameKey: int, userKey: int):
        await websocket.accept()
        res = requests.post(
            BACKEND_URL + 'group/on-connect/',
            json={
                'gameKey': gameKey,
                'userKey': userKey
            }
        )
        print(res)
        self.connections[userKey] = websocket

    def disconnect(self, userKey):
        self.connections.pop(userKey)

    async def send(self, userKey, data):
        await self.connections[userKey].send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()