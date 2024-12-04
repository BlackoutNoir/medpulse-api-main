from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
import uuid
from app.db.enums import user_type as UserType, auth_type as AuthType, gender_type, action_type, entity_type


# Base models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    phone_no: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_verified: bool = False
    is_active: bool = True
    user_type: UserType
    gender: Optional[gender_type] = None
    country: Optional[str] = None
    city: Optional[str]  = None
    street_address: Optional[str] = None 
    zip_code: Optional[str]  = None



class SettingsBase(BaseModel):
    font_size: int = 14
    screen_reader: bool = False
    on_screen_keyboard: bool = False
    email_notifications: bool = True
    sms_notifications: bool = False
    email_reminders: bool = False
    sms_reminders: bool = False
    auth_type: AuthType = AuthType.none



# Create models

class SettingsCreate(SettingsBase):
    user_uid: uuid.UUID = None  

 

class UserCreate(UserBase):
    password: str

# Update models

class SettingsUpdate(SettingsBase):
    font_size: Optional[int] = None
    screen_reader: Optional[bool] = None
    on_screen_keyboard: Optional[bool] = None
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    email_reminders: Optional[bool] = None
    sms_reminders: Optional[bool] = None
    auth_type: Optional[AuthType] = None

class UserUpdate(UserBase):    
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    is_verified: Optional[bool] = None
    phone_no: Optional[str] = None
    gender: Optional[gender_type] = None
    is_active: Optional[bool] = None
    user_type: Optional[UserType] = None
    settings: Optional[SettingsUpdate] = None

# Response Model 

class SettingsResponse(SettingsBase):
    uid: uuid.UUID
 
    model_config = {
        "from_attributes": True
    }

class ChatResponse(BaseModel):
    uid: uuid.UUID
    name: str

class LogResponse(BaseModel):
    uid: uuid.UUID
    action: action_type
    entity: entity_type
    description: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }



class UserResponse(UserBase):
    uid: uuid.UUID
    
    created_at: datetime
    updated_at: datetime
    last_login: datetime

    settings: SettingsResponse

    logs: List[LogResponse]

    chats: List[ChatResponse]

    model_config = {
        "from_attributes": True
    }

# filter

class UserFilter(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone_no: Optional[str] = None
    gender: Optional[gender_type] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    user_type: Optional[UserType] = None
    date_of_birth: Optional[date] = None
    created_at: Optional[date] = None
    order_by: Optional[str] = None

#nested 
class UserNested(UserBase):
    uid: uuid.UUID
    model_config = {
        "from_attributes": True
    }