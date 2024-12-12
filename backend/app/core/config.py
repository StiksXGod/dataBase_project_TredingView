from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")
    SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES_FOR_PROD"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    ALLOWED_CHARACTERS = set(os.getenv("ALLOWED_CHARACTERS"))
    MAX_SIZE_POOL = int(os.getenv("MAX_SIZE_POOL"))
    MIN_SIZE_POOL = int(os.getenv("MIN_SIZE_POOL"))


    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True