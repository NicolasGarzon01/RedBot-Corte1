from fastapi import FastAPI
from .database import Base, engine
from .accounts import routes as account_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Account Service")

app.include_router(account_routes.router)
