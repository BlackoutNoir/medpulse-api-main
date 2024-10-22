from fastapi import FastAPI
from backend.app.api.routes import user  
from database import engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/api")


  