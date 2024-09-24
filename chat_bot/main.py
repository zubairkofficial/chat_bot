from contextlib import asynccontextmanager
from fastapi import  FastAPI
from sqlmodel import SQLModel
from starlette.config import Config
from starlette.datastructures import Secret
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



        
# app.include_router(chat)
app.include_router(router)
app.include_router(chat_router)
app.include_router(conversation_router)

# Example route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


