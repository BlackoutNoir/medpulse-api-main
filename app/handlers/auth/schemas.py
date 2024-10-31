from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid

class UserBase(BaseModel):
    username: str =  Field(min_length=3, max_length=8)
    email: EmailStr = Field(max_length=50)
    firstname: str
    lastname: str



class UserCreate(UserBase):
    password: str = Field(min_length=8)


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