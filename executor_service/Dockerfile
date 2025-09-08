FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Instala las herramientas necesarias
RUN apt-get update && apt-get install -y dos2unix netcat-openbsd

# Copia, convierte y da permisos al script
COPY wait-for-db.sh /wait-for-db.sh
RUN dos2unix /wait-for-db.sh && chmod +x /wait-for-db.sh

# ▼▼▼ LÍNEA CMD CORREGIDA Y SIMPLIFICADA ▼▼▼
CMD ["/wait-for-db.sh", "db", "python", "-m", "app.executor.worker"]