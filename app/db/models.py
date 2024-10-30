from enum import Enum
from sqlmodel import  SQLModel, Field, Column
import uuid
import sqlalchemy.dialects.postgresql as pg

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