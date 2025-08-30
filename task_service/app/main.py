from fastapi import FastAPI
from .database import Base, engine
from .tasks import routes as task_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Service")
app.include_router(task_routes.router)
