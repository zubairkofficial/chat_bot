from pydantic import BaseModel


class CreateConversation(BaseModel):
   chat_id:int
   user_message:str
    
class Config:
     orm_mode = True