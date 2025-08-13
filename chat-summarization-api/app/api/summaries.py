from fastapi import APIRouter, HTTPException, status
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/summarize")
async def summarize_conversation(conversation_id: str):
    """Generate summary and insights for a conversation"""
    chat_service = ChatService()
    llm_service = LLMService()
    
    try:
        # Get conversation messages
        messages = await chat_service.get_conversation_messages(conversation_id)
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No messages found for this conversation"
            )
            
        # Extract message content
        message_contents = [msg["content"] for msg in messages]
        
        # Generate summary and insights
        summary = await llm_service.generate_summary(message_contents)
        insights = await llm_service.generate_insights(message_contents)
        
        return {
            "conversation_id": conversation_id,
            "summary": summary,
            "insights": insights
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )