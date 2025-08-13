from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    conversation_id: str
    user_id: str
    content: str
    timestamp: datetime = datetime.now()
    metadata: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "user_id": "user_1",
                "content": "Hello there!",
                "timestamp": "2023-01-01T12:00:00",
                "metadata": {"platform": "web"}
            }
        }