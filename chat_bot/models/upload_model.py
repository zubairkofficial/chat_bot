from typing import Dict
from sqlmodel import SQLModel, Field,Column
from sqlalchemy import JSON
from datetime import datetime, timezone

class FileData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content :str
    vector: bytes  
    file_name :str
    upload_time: datetime = Field(default_factory=datetime.now(timezone.utc))
