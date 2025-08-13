from fastapi import APIRouter, WebSocket
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
import json

router = APIRouter()

@router.websocket("/summary")
async def websocket_summary(websocket: WebSocket):
    """WebSocket endpoint for real-time summarization"""
    await websocket.accept()
    chat_service = ChatService()
    llm_service = LLMService()
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            if "conversation_id" not in payload:
                await websocket.send_json({"error": "conversation_id required"})
                continue
                
            messages = await chat_service.get_conversation_messages(
                payload["conversation_id"]
            )
            
            if not messages:
                await websocket.send_json({"error": "No messages found"})
                continue
                
            # Send periodic updates
            message_contents = [msg["content"] for msg in messages]
            summary = await llm_service.generate_summary(message_contents)
            await websocket.send_json({"summary": summary})
            
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)