from pydantic import BaseModel # type: ignore

class CreateChat(BaseModel):
   phone_number:str
    
class Config:
     orm_mode = True