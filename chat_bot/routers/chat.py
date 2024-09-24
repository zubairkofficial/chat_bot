from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from chat_bot.models.chat import Chat
from chat_bot.setting import engine, get_session
from chat_bot.schema import chat_schems
from sqlmodel import  Session, select


chat_router = APIRouter()


@chat_router.post("/phone_number",response_model=Chat)
def create_number(input: chat_schems.CreateChat = Body(), session: Session = Depends(get_session)):
 try:
    existing_chat = session.exec(select(Chat).where(Chat.phone_number == input.phone_number)).first()
    
    if existing_chat is not None:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    new_number = Chat(**input.model_dump())

    session.add(new_number)

    session.commit()

    session.refresh(new_number)

    return new_number
 except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))