
from fastapi import FastAPI
from .database import Base, engine
from .users import routes as user_routes
from .models import User

Base.metadata.create_all(bind=engine)


app = FastAPI(title="User Service - SOA")
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
    return {"message": "User service is running"}

app.include_router(user_routes.router, tags=["users"])
