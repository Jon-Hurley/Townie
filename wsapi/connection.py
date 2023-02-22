from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import requests

BACKEND_URL = "http://127.0.0.1:8000/"

class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, websocket: WebSocket, lobby_key: int, client_key: int):
        await websocket.accept()
        requests.post(
            BACKEND_URL + '/group/on-connect',
            data={
                'lobby_key': lobby_key,
                'client_key': client_key
            }
        )
        self.connections[client_key] = websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()