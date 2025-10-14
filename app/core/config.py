from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings and loads them from a .env file.
    """
    DATABASE_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    STORAGE_PATH: str = "storage"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

# Create a single, globally accessible instance of the settings.
settings = Settings()