from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils import in_container


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    entrypoint: str = "main:app"
    
class ApiConfig(BaseModel):
    prefix: str = "/api"
    message: str = "Welcome to DnD Character Manager API"
    
class CORSConfig(BaseModel):
    origins: list = ["*"]
    methods: list = ["*"]
    headers: list = ["*"]
    credentials: bool = True

class PostgresConfig(BaseModel):
    host: str | None = None
    port: str | None = None
    user: str | None = None
    password: str | None = None
    db: str | None = None
    service: str | None = None
    
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    
    @computed_field
    @property
    def url(self) -> str:            
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.service if in_container() else self.host + ':' + self.port}/{self.db}"      

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(".env"), 
        env_nested_delimiter="_",
        env_file_encoding="utf-8", 
        extra="ignore"
    )
    
    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    cors: CORSConfig = CORSConfig()
    postgres: PostgresConfig = PostgresConfig()

settings = Settings()