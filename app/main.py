from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import api_router
from app.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Medpulse API is up")
    await init_db()
    yield
    print("Medpulse API is down")


version = "v1"

app = FastAPI(
    title="Medpulse",
    version=version,
    lifespan=lifespan
)

app.include_router(api_router, prefix=f"/api/{version}")