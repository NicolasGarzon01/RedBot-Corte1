from fastapi import FastAPI
from .database import Base, engine
from .tasks import routes as task_routes
from .models import Task
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Service")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Se añade el prefijo /api para que coincida con la configuración de NGINX.
app.include_router(task_routes.router, prefix="/api")