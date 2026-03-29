from fastapi import WebSocket
from typing import List
import json


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast a new signal alert to all connected clients."""
        text = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(text)
            except Exception:
                self.active_connections.remove(connection)

    async def send_to(self, websocket: WebSocket, message: dict):
        await websocket.send_text(json.dumps(message))


ws_manager = WebSocketManager()
