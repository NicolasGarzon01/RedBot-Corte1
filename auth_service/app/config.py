import os
from dotenv import load_dotenv

load_dotenv()

# Base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30
