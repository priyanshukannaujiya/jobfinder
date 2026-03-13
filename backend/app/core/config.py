from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

db_path = os.path.join(BASE_DIR, "jobs.db")
default_db_url = f"sqlite:///{db_path}"

class Settings(BaseSettings):
    PROJECT_NAME: str = "JobMaker API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", default_db_url)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

settings = Settings()
