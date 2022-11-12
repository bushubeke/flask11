import os
from pydantic import BaseSettings 

class Settings(BaseSettings):
    SQLITE_SYNC_URL_PREFIX :str = os.environ.get("SQLITE_SYNC_URL_PREFIX")
    SQLALCHEMY_DATABASE_URI:str = os.environ.get("SQLITE_SYNC_URL_PREFIX")
    SQLITE_ASYNC_URL_PREFIX :str = os.environ.get("SQLITE_ASYNC_URL_PREFIX")
    POSTGRES_SYNC_URL :str = os.environ.get("POSTGRES_SYNC_URL")
    PG_URL :str = os.environ.get("PG_URL")
    POSTGRES_ASYNC_URL :str = os.environ.get("POSTGRES_ASYNC_URL")
    SECRET_KEY : str = os.environ.get("SECRET_KEY")
    JWT_APP_TOKEN_EXPIRE_TIME :int =4
    JWT_REFRESH_TOKEN_EXPIRE_TIME :int =5
    DEBUG : bool=False
    
    class Config:
        env_file = ".env"

settings = Settings()