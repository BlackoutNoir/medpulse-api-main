from enum import Enum
from sqlmodel import  SQLModel, Field, Column
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from typing import Optional



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

    user_type: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="patient")
    )


    def __repr__(self):
        return f"<User {self.username}>"
    

class AuthType(str, Enum):
    email = "email"
    sms = "sms"
    none = "none"

class Settings(SQLModel, table=True):
    __tablename__ = "settings"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    font_size: int = Field(default=14)
    screen_reader: bool = Field(default=False)
    on_screen_keyboard: bool = Field(default=False)
    email_notifications: bool = Field(default=True)
    sms_notifications: bool = Field(default=False)
    email_reminders: bool = Field(default=False)
    sms_reminders: bool = Field(default=False)
    auth_type: AuthType = Field(nullable=False)

class Log:
    pass

class Chat:
    pass

class Admin:
    pass

class Staff:
    pass

class Patient:
    pass

class Pages:
    pass

class Department:
    pass

class Bill:
    pass

class Appointment:
    pass

class Labtest:
    pass

class Prescription:
    pass

class Medication:
    pass

class Allergies:
    pass

class Diagnosis:
    pass
