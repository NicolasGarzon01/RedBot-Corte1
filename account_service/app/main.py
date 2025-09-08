
from fastapi import FastAPI
from .database import Base, engine
from .accounts import routes as account_routes
from .models import Account

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Account Service")
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(account_routes.router)
