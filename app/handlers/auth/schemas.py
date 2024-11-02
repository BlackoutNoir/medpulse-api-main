from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional
import uuid

class UserBase(BaseModel):
    username: str =  Field(min_length=3, max_length=8)
    email: EmailStr = Field(max_length=50)
    firstname: str
    lastname: str



class UserCreate(UserBase):
    password_hash: str = Field(min_length=8)


class UserUpdate(UserBase):
    
    username: Optional[str] = Field(min_length=3, max_length=8)
    email: Optional[EmailStr] = Field(max_length=50)
    firstname: Optional[str]
    lastname: Optional[str]
    password: Optional[str] = Field(min_length=8)

class UserResponse(UserBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str 

    @model_validator(mode="before")
    def check_email_or_username(cls, values):
        if not values.get("email") and not values.get("username"):
            raise ValueError("Either email or username must be provided")
        return values