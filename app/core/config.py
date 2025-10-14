from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    STORAGE_PATH: str = "storage"

    class Config:
        env_file = ".env"

settings = Settings()