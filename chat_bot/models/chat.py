from sqlmodel import SQLModel, Field, Relationship
from typing import  Optional
from datetime import datetime  # For proper datetime handling
from chat_bot.models.conversation import Conversation

class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


    class Config:
        orm_mode = True