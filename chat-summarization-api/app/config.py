from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "chat_db"
    OPENAI_API_KEY: str
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()