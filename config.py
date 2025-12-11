# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # SMTP Email Settings
    SMTP_HOST: str = "smtp.gmail.com"       # default, can override in .env
    SMTP_PORT: int = 587                     # default TLS port
    SMTP_EMAIL: str                           # your sending email
    SMTP_PASSWORD: str                        # your email password / app password

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"   # loads variables from .env

settings = Settings()
