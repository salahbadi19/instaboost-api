# admin_api/routers/chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter(prefix="/api/chat", tags=["chat"])

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

@router.websocket("/support")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # رسالة ترحيب تلقائية عند الاتصال
        await manager.send_personal_message("مرحباً! كيف يمكنني مساعدتك اليوم؟", websocket)
        while True:
            data = await websocket.receive_text()
            # هنا يمكنك إرسال الرسالة إلى فريق الدعم (في الإنتاج: احفظها أو أرسلها لمسؤول)
            # الآن نُعيد إرسالها كـ "رد تلقائي" للمستخدم
            await manager.send_personal_message(
                "شكراً لرسالتك! سنتواصل معك قريباً.", websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
