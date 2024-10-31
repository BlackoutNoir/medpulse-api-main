from datetime import datetime,date
from enum import Enum
from typing import Optional
from sqlmodel import  SQLModel, Field, Column
import uuid
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "medpulse_user"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    username: str 
    email: str
    firstname: str
    lastname: str
    phone_no: Optional[str] = Field(default=None, nullable=True)
    date_of_birth:  Optional[date] = Field(default=None, nullable=True)
    is_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  
    last_login: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    password_hash: str = Field(exclude=True)
    def __repr__(self):
        return f"<User {self.username}>"
    