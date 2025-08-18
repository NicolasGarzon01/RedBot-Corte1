import os
from dotenv import load_dotenv

load_dotenv()

# Base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

# Configuración JWT
JWT_SECRET = os.getenv("JWT_SECRET", "cambia-esto-por-un-secreto-largo")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30
