from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from app.db.enums import action_type , entity_type 



# Base model
class LogBase(BaseModel):
    action: action_type
    entity: entity_type
    description: str


# Create model
class LogCreate(LogBase):
    user_uid: uuid.UUID
    pass

# Update model
class LogUpdate(LogBase):
    action: Optional[action_type] = None
    entity: Optional[entity_type] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None

# Response model
class UserResponse(BaseModel):
    uid: uuid.UUID
    username: str

    model_config = {
        "from_attributes": True
    }

class LogResponse(LogBase):
    timestamp: datetime 
    uid: uuid.UUID  
    user_uid: uuid.UUID


    user: UserResponse

    model_config = {
        "from_attributes": True
    }

# Filter model
class LogFilter(LogBase):
    action: Optional[action_type] = None
    entity: Optional[entity_type] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None
    user_uid: Optional[uuid.UUID] = None
    order_by: Optional[str] = None
