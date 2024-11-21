from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


# Base model
class ChatBase(BaseModel):
    name: str

class MessageBase(BaseModel):
    timestamp: datetime 
    is_read: bool
    message_content: str

class UserBase(BaseModel):
    pass


# Create model
class MessageCreate(MessageBase):
    sender_id: uuid.UUID
    chat_id: uuid.UUID

class UserCreate(UserBase):
    uid : uuid.UUID

class ChatCreate(ChatBase):
    participants: list[UserCreate]
    pass


# Update model

class MessageUpdate(MessageBase):
    sender_id: uuid.UUID
    chat_id: uuid.UUID
    message_content: str
    
class UserUpdate:
    uid: Optional[uuid.UUID] = None

class ChatUpdate(ChatBase):
    name: Optional[str] = None



# Response model
class UserResponse(UserBase):
    uid: uuid.UUID
    firstname: str
    lastname: str
    username: str
    image_url: str
    

    model_config = {
        "from_attributes": True
    }

class messageResponse(MessageBase):
    uid: uuid.UUID
    sender_id: uuid.UUID
    chat_id: uuid.UUID

class ChatResponse(ChatBase):
    uid: uuid.UUID
    name: str
    messages : list[messageResponse]
    participants: list[UserResponse]
    model_config = {
        "from_attributes": True
    }

# Filter model
class ChatFilter(ChatBase):
    uid: Optional[str] = None
    name: Optional[str] = None
    order_by: Optional[str] = None


