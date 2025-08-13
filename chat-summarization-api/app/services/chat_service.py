from typing import List
from datetime import datetime
from app.database import get_database
from app.models.chat import ChatMessage
from fastapi import HTTPException, status

class ChatService:
    def __init__(self):
        self.db = get_database()
        self.chats_collection = self.db["chats"]

    async def create_chat_message(self, message: ChatMessage) -> str:
        """Insert single chat message"""
        result = await self.chats_collection.insert_one(message.dict())
        return str(result.inserted_id)

    async def create_chat_batch(self, messages: List[ChatMessage]) -> int:
        """Bulk insert chat messages"""
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No messages provided"
            )
        
        documents = [msg.dict() for msg in messages]
        result = await self.chats_collection.insert_many(documents)
        return len(result.inserted_ids)

    async def get_conversation_messages(
        self, 
        conversation_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """Retrieve messages for a conversation with pagination"""
        cursor = self.chats_collection.find(
            {"conversation_id": conversation_id}
        ).skip(skip).limit(limit).sort("timestamp", 1)
        
        return await cursor.to_list(length=limit)

    async def delete_conversation(self, conversation_id: str) -> int:
        """Delete all messages in a conversation"""
        result = await self.chats_collection.delete_many(
            {"conversation_id": conversation_id}
        )
        return result.deleted_count