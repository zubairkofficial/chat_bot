from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: Optional[int] = Field(default=None, foreign_key="chat.id")
    user_message:str
    chatbot_message:str
    timestamp: Optional[datetime] = Field(default_factory=datetime.now(timezone.utc))

    class Config:
        orm_mode = True