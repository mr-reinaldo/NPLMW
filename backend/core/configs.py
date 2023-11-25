from pydantic_settings import BaseSettings
from typing import ClassVar

from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    """Settings class."""

    # Variáveis da API.
    PROJECT_NAME: str = getenv("PROJECT_NAME")
    PROJECT_DESCRIPTION: str = getenv("PROJECT_DESCRIPTION")
    PROJECT_VERSION: str = getenv("PROJECT_VERSION")
    API_V1_STR: str = getenv("API_V1_STR")

    # Variáveis do banco de dados.
    DB_URL: str = getenv("DB_URL")
    DBBaseModel: ClassVar = declarative_base()

    # Variáveis do JWT.
    JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = getenv("JWT_ALGORITHM")
    JWT_EXPIRE_MINUTES: int = getenv("JWT_EXPIRE_MINUTES")
    TIMEZONE: str = getenv("TIMEZONE")

    # Variáveis do CORS.
    # ALLOWED_HOSTS: list = getenv("ALLOWED_HOSTS")
    
    class Config:
        """Config class."""

        case_sensitive = True


settings = Settings()