#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/20/2019 3:24 PM
# @File    : route.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.


from typing import List

from EdgeGPT import Chatbot
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from eagle.apps import app
from eagle.etc.settings import COOKIES

router = APIRouter(
    prefix="/chat",
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("/aa")
async def get():
    return HTMLResponse('')


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        bot = Chatbot(cookies=COOKIES)
        while True:
            data = await websocket.receive_text()
            wrote = 0
            async for final, response in bot.ask_stream(
                prompt=data,
                conversation_style=["creative", "balanced", "precise"][0],
            ):
                if not final:
                    print(response[wrote:], end="")
                    await manager.send_personal_message(f"You wrote: {response[wrote:]}", websocket)
                    await manager.broadcast(f"Client #{client_id} says: {response[wrote:]}")
                    wrote = len(response)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
