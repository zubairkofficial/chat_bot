from pydantic import BaseModel # type: ignore
from typing import Optional
class CreateTodo(BaseModel):
    content: str
    isActive:Optional[bool]
class UpdateTodo(BaseModel):
    content: Optional[str]
    isActive:Optional[bool]

    


    class Config:
        orm_mode = True
