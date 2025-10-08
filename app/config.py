import os
from dotenv import load_dotenv
from pathlib import Path

# Try to load .env file from multiple locations
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)
load_dotenv(override=True)  # Also try current directory

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip("'\"").strip()
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./student_buddy.db")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Gemini Configuration
    GEMINI_MODEL: str = "gemini-2.5-flash"  # Latest Gemini model
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    
    # Application Configuration
    MAX_CONTENT_LENGTH: int = 8000  # characters
    DEFAULT_QUIZ_QUESTIONS: int = 5
    API_TIMEOUT: int = 60  # seconds

settings = Settings()