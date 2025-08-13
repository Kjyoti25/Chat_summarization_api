from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, ChatMessagesBatch
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/", response_model=List[str])
async def create_chat_batch(batch: ChatMessagesBatch):
    """Store multiple chat messages"""
    chat_service = ChatService()
    messages = [
        ChatMessage(
            conversation_id=batch.conversation_id,
            user_id=batch.user_id,
            content=msg.content,
            metadata=msg.metadata
        ) for msg in batch.messages
    ]
    
    try:
        inserted_ids = await chat_service.create_chat_batch(messages)
        return {"inserted_ids": inserted_ids}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{conversation_id}", response_model=List[ChatMessageResponse])
async def get_conversation(
    conversation_id: str,
    skip: int = 0,
    limit: int = 100
):
    """Retrieve conversation messages"""
    chat_service = ChatService()
    try:
        messages = await chat_service.get_conversation_messages(
            conversation_id, skip, limit
        )
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation not found: {str(e)}"
        )

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    chat_service = ChatService()
    deleted_count = await chat_service.delete_conversation(conversation_id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No messages found for this conversation"
        )
    return {"deleted_count": deleted_count}