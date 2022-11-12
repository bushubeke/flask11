import os
# from pydantic import BaseSettings 
class Config(object):
    # class Settings(BaseSettings):
    SECRET_KEY : str = os.getenv("SECRET_KEY")
    

class DevConfig(Config):
    SQLITE_SYNC_URL_PREFIX :str = os.getenv("SQLITE_SYNC_URL_PREFIX")
    SQLALCHEMY_DATABASE_URI:str = os.getenv("SQLITE_SYNC_URL_PREFIX")
    SQLITE_ASYNC_URL_PREFIX :str = os.getenv("SQLITE_ASYNC_URL_PREFIX")
    POSTGRES_SYNC_URL :str = os.getenv("POSTGRES_SYNC_URL")
    PG_URL :str = os.getenv("PG_URL")
    POSTGRES_ASYNC_URL :str = os.getenv("POSTGRES_ASYNC_URL")
    JWT_APP_TOKEN_EXPIRE_TIME :int =4
    JWT_REFRESH_TOKEN_EXPIRE_TIME :int =5
    DEBUG : bool=False
        
config_by_name = dict(
    dev=DevConfig
)

key = Config.SECRET_KEY
#     class Config:
#         env_file = ".env"

# settings = Settings()