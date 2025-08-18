from fastapi import FastAPI
from .database import Base, engine
from .users import routes as user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service - SOA")
app = FastAPI(debug=True)   

@app.get("/")
def root():
    return {"message": "User service is running"}

app.include_router(user_routes.router, tags=["users"])
