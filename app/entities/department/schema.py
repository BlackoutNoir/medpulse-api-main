from pydantic import BaseModel
from typing import Optional, List
import uuid


# 
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    default_appointment_time: int


# creation model
class DepartmentCreate(DepartmentBase):
    pass


# update model
class DepartmentUpdate(DepartmentBase):
    name: Optional[str] = None
    description: Optional[str] = None
    default_appointment_time: Optional[int] = None


# response models
class DepartmentResponse(DepartmentBase):
    uid: uuid.UUID
    staff: List["StaffResponse"]

    model_config = {
        "from_attributes": True
    }
    
class StaffResponse(BaseModel):
    uid: uuid.UUID
    role: str
    user : "UserResponse"

    model_config = {
        "from_attributes": True
    }


class UserResponse(BaseModel):
    uuid: uuid.UUID
    firstname: str
    lastname: str
    email: str
    image_url: str

    model_config = {
        "from_attributes": True
    }


#filter
class DepartmentFilter(BaseModel):
    uid : Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    default_appointment_time: Optional[int] = None
    order_by: Optional[str] = None