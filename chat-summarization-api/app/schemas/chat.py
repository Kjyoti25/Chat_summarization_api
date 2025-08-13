from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    content: str
    metadata: Optional[dict] = None

class ChatMessageResponse(BaseModel):
    id: str
    conversation_id: str
    user_id: str
    content: str
    timestamp: datetime
    metadata: Optional[dict]

    class Config:
        orm_mode = True

class ChatMessagesBatch(BaseModel):
    conversation_id: str
    user_id: str
    messages: List[ChatMessageCreate]