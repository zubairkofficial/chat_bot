from openai import OpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from pydantic import Secret
from chat_bot.main import API_KEY
from starlette.config import Config


config = Config(".env")

API_KEY = config("OPENAI_API_KEY", cast=Secret, default=None)

if not API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment or .env file.")


llm = OpenAI(api_key=str(API_KEY))

# Create a prompt template
prompt_template = PromptTemplate(template="You are a helpful assistant. Answer the question: {question}")

# Create the LangChain model
chain = LLMChain(llm=llm, prompt=prompt_template)