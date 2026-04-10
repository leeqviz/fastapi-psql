import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVICE: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    @property
    def in_container(self) -> bool:
        return os.path.exists("/.dockerenv")
    
    @property
    def database_url(self) -> str:
        if self.in_container:
            path = self.POSTGRES_SERVICE
        else:
            path = self.POSTGRES_HOST + ":" + self.POSTGRES_PORT
        
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{path}/{self.POSTGRES_DB}"

settings = Settings()