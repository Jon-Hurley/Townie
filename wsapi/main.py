from fastapi import Request, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from wsapi.connection import manager
from pydantic import BaseModel
import json
import asyncio

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse()

@app.post("/update/")
async def updateUser(request: Request):
    body = await request.json()
    userKey = body['userKey']
    game = body['game']
    # print("Updating user", userKey, "with:", game)
    manager.send(userKey, game)
    return JSONResponse({}) 

@app.websocket("/ws/{gameKey}/{userKey}")
async def websocket_endpoint(websocket: WebSocket, gameKey: int, userKey: int):
    await manager.connect(websocket, gameKey, userKey)
    try:
        while True:
            data = await websocket.receive_json()
            await asyncio.sleep(30)
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_key} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_key} left the chat")