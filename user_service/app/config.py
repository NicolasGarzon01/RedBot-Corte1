import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

JWT_SECRET = os.getenv("JWT_SECRET", "cambia-esto-por-un-secreto-largo")
JWT_ALGORITHM = "HS256"
