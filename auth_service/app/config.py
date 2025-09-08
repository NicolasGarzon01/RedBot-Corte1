import os
from dotenv import load_dotenv

# Carga las variables de un archivo .env (útil para pruebas locales)
load_dotenv()

# --- Configuración de la Base de Datos ---
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Configuración de JWT (Tokens) ---
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
# 👇 VARIABLE AÑADIDA (con un valor por defecto de 30 minutos)
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

# --- Verificación ---
# Nos aseguramos de que todas las variables necesarias estén cargadas
if not DATABASE_URL or not SECRET_KEY or not JWT_ALGORITHM:
    raise ValueError("Una o más variables de entorno críticas (DATABASE_URL, SECRET_KEY, JWT_ALGORITHM) no están definidas.")
