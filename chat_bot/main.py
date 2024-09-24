from contextlib import asynccontextmanager
from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, select
from starlette.config import Config
from starlette.datastructures import Secret
from chat_bot.schema import chat_schems, conversation_schems
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from chat_bot.routers.upload_file import  router
from chat_bot.routers.chat import  chat_router
from chat_bot.routers.conversation import  conversation_router
from chat_bot.setting import engine

config = Config(".env")

API_KEY = config("OPENAI_API_KEY", cast=Secret, default=None)

if not API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment or .env file.")


def init_db():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize the database tables
    yield  # Allows the app to run

app = FastAPI(lifespan=lifespan)


llm = OpenAI(api_key=str(API_KEY))

# Create a prompt template
prompt_template = PromptTemplate(template="You are a helpful assistant. Answer the question: {question}")

# Create the LangChain model
chain = LLMChain(llm=llm, prompt=prompt_template)

# Dependency to provide session management

        
# app.include_router(chat)
app.include_router(router)
app.include_router(chat_router)
app.include_router(conversation_router)

# Example route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}




    
# def cosine_similarity(vec1, vec2):
#     dot_product = np.dot(vec1, vec2)
#     norm_a = np.linalg.norm(vec1)
#     norm_b = np.linalg.norm(vec2)
#     return dot_product / (norm_a * norm_b)

# @app.post("/conversations/")
# async def create_conversation(
#     input: conversation_schems.CreateConversation = Body(), 
#     session: Session = Depends(get_session)
# ):
#     try:
#         # Retrieve all records from the database
#         results = session.exec(select(FileData)).all()

#         if not results:
#             raise HTTPException(status_code=404, detail="No JSON file found in the database")

#         # Create embeddings
#         embeddings = OpenAIEmbeddings()
#         query_vector = embeddings.embed_query(input.user_message)

#         # Initialize variables for tracking the best match
#         best_match = None
#         highest_similarity = 0

#         # Calculate similarities
#         for file_data in results:
#             stored_vector = np.frombuffer(file_data.vector, dtype=np.float32)
#             similarity = cosine_similarity(query_vector, stored_vector)
            
#             # Check if this similarity is the highest found so far
#             if similarity > highest_similarity:
#                 highest_similarity = similarity
#                 best_match = {
#                     "file_name": file_data.file_name,
#                     "content": json.loads(file_data.content),
#                     "similarity": similarity
#                 }

#         if highest_similarity > 0.7:  # Return the best match only if above threshold
#             new_conversation = Conversation(
#                 chat_id=input.chat_id,
#                 user_message=input.user_message,
#                 chatbot_message=json.dumps(best_match),
#                 timestamp=datetime.now(timezone.utc)
#             )

#             # Add and commit the new conversation to the session
#             session.add(new_conversation)
#             session.commit()
#             session.refresh(new_conversation)  # Refresh to get generated ID and other details

#             return  best_match

#         else:
#             return {"detail": "No matching documents found above the similarity threshold."}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))