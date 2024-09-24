from sqlalchemy import create_engine
from sqlmodel import Session
from starlette.config import Config
from starlette.datastructures import Secret

# Load .env file if available, otherwise environment variables are used
config = Config(".env")

PG_DATABASE_URL = config("PG_DATABASE_URL", cast=Secret, default=None)


engine = create_engine(str(PG_DATABASE_URL), pool_recycle=300, pool_size=10, echo=True)

def get_session():
    session = Session(engine)
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
# Optional: handle case if DATABASE_URL is not provided
if PG_DATABASE_URL is None:
    raise ValueError("PG_DATABASE_URL is not set in the environment or .env file.")
