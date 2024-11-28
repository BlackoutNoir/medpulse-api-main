from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import api_router
from app.db.main import init_db
from app.db.blocklist import cleanup_blocklist
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from app.db.config import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Medpulse API is up")
    cleanup_task = asyncio.create_task(cleanup_blocklist())
    await init_db()
    yield
    print("Medpulse API is down")




version = "v1"

app = FastAPI(
    title="Medpulse",
    version=version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.FRNT_END_URL,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)



app.include_router(api_router, prefix=f"/api/{version}")