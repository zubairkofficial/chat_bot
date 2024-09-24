from fastapi import APIRouter, Body, Depends, HTTPException
import numpy as np
from sqlmodel import Session
from chat_bot.models.chat import Chat
from chat_bot.models.conversation import Conversation
from chat_bot.models.upload_model import FileData
from chat_bot.setting import engine, get_session
from chat_bot.schema import chat_schems, conversation_schems
from sqlmodel import  Session, select
from langchain.embeddings.openai import OpenAIEmbeddings
import json
from datetime import datetime, timezone


conversation_router = APIRouter()


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    return dot_product / (norm_a * norm_b)

@conversation_router.post("/conversations/")
async def create_conversation(
    input: conversation_schems.CreateConversation = Body(), 
    session: Session = Depends(get_session)
):
    try:
        results = session.exec(select(FileData)).all()

        if not results:
            raise HTTPException(status_code=404, detail="No JSON file found in the database")

        embeddings = OpenAIEmbeddings()
        query_vector = embeddings.embed_query(input.user_message)

        best_match = None
        highest_similarity = 0

        for file_data in results:
            stored_vector = np.frombuffer(file_data.vector, dtype=np.float32)
            similarity = cosine_similarity(query_vector, stored_vector)
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = {
                    "file_name": file_data.file_name,
                    "content": json.loads(file_data.content),
                    "similarity": similarity
                }

        if highest_similarity > 0.7: 
            new_conversation = Conversation(
                chat_id=input.chat_id,
                user_message=input.user_message,
                chatbot_message=json.dumps(best_match),
                timestamp=datetime.now(timezone.utc)
            )

            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation) 

            return  best_match

        else:
            return {"detail": "No matching documents found above the similarity threshold."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))