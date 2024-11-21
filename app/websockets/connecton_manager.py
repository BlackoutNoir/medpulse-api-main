from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict, Annotated

class ChatConnectionManager:
    def __init__(self):
        # A dictionary where the keys are chat_ids and the values are lists of active connections for that chat.
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, chat_id: str, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: str, websocket: WebSocket):
        self.active_connections[chat_id].remove(websocket)
        if not self.active_connections[chat_id]: 
            del self.active_connections[chat_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, chat_id: str, message: str):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_text(message)

manager = ChatConnectionManager()

def get_connection_manager():
    return manager


chat_connection = Annotated[ChatConnectionManager, Depends(get_connection_manager)]