from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from app.db.config import Config
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import Annotated


engine : AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    future=True
)
    
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

db_session = Annotated[AsyncSession, Depends(get_async_session)]

async def init_db() -> None:
    async with engine.begin() as conn:
        pass
        # from app.db.models import Settings, User
        # await conn.run_sync(SQLModel.metadata.create_all)


  