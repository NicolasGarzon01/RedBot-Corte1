from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .auth import routes as auth_routes

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Auth Service - SOA")

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

