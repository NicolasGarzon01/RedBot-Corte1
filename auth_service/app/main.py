
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .auth import routes as auth_routes
from .auth.models import User

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Auth Service - SOA")
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Auth service is running"}
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # tu frontend real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

