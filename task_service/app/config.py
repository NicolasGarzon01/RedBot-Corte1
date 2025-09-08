import os
from dotenv import load_dotenv

load_dotenv()

# --- Carga toda la configuración desde el entorno ---
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# --- Verificación ---
if not DATABASE_URL or not SECRET_KEY or not JWT_ALGORITHM:
    raise ValueError("Faltan variables de entorno críticas: DATABASE_URL, SECRET_KEY, JWT_ALGORITHM")
