from fastapi import APIRouter,File,  UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from chat_bot.models.upload_model import FileData
import json
from chat_bot.setting import engine, get_session
from langchain.embeddings.openai import OpenAIEmbeddings
import numpy as np


router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), session: Session = Depends(get_session)):
 try:
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed")

    content = await file.read()
    try:
        json_data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

    embeddings = OpenAIEmbeddings()
    
    vectors = embeddings.embed_documents([json.dumps(doc) for doc in json_data])
    with Session(engine) as session:
     for doc, vector in zip(json_data, vectors):
        vector_bytes = np.array(vector).astype(np.float32).tobytes()  
        new_file_data = FileData(
            file_name=file.filename,          
            content=json.dumps(doc),          
            vector=vector_bytes                
        )
        session.add(new_file_data)
        session.commit()

    return {"filename": file.filename, "detail": "File uploaded and processed successfully"}
 except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))