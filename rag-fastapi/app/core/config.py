from pathlib import Path
import os

from dotenv import load_dotenv

# Load the project's .env file explicitly so config works from any working directory.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_FILE)


class Settings:
    # Basic app settings. DEBUG is normalized so "true" and "True" both work.
    APP_NAME: str = os.getenv("APP_NAME", "RAG API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Auth settings use safe defaults so missing env values don't break imports.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # OpenAI is optional because this project currently uses Ollama.
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Ollama settings are read from .env instead of being hardcoded in services.
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

    # PostgreSQL is required for this app now; startup should fail fast if it is missing.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")


settings = Settings()
