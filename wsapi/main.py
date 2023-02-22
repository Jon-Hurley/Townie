from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from connection import manager

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse()

@app.websocket("/ws/{lobby_key}/{client_key}")
async def websocket_endpoint(websocket: WebSocket, lobby_key: int, client_key: int):
    await manager.connect(websocket, lobby_key, client_key)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_key} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_key} left the chat")