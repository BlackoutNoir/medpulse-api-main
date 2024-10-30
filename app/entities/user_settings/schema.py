from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid

class AuthType(str, Enum):
    email = "email"
    sms = "sms"
    none = "none"

class SettingsBase(BaseModel):
    font_size: Optional[int] = Field(default=14)
    screen_reader: Optional[bool] = Field(default=False)
    on_screen_keyboard: Optional[bool] = Field(default=False)
    email_notifications: Optional[bool] = Field(default=True)
    sms_notifications: Optional[bool] = Field(default=False)
    email_reminders: Optional[bool] = Field(default=False)
    sms_reminders: Optional[bool] = Field(default=False)
    auth_type: AuthType

class SettingsCreate(SettingsBase):
    pass

class SettingsUpdate(SettingsBase):
    font_size: Optional[int] = None
    screen_reader: Optional[bool] = None
    on_screen_keyboard: Optional[bool] = None
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    email_reminders: Optional[bool] = None
    sms_reminders: Optional[bool] = None
    auth_type: Optional[AuthType] = None


class SettingsResponse(SettingsBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }