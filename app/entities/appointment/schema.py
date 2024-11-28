from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
from app.db.enums import appointment_status_type

    
# Base model
class AppointmentBase(BaseModel):

    start_date: datetime 
    duration: int # in minutes 
    is_checked_in: bool 
    status: Optional[appointment_status_type] = appointment_status_type.PENDING
    reason_for_visit: Optional[str] = None
    location: str
    is_virtual: Optional[bool] = None
    details: Optional[str] = None
    patient_uid: uuid.UUID 
    doctor_uid: uuid.UUID 


# creation model
class AppointmentCreate(AppointmentBase):
    pass

# update model
class AppointmentUpdate(AppointmentBase):
    start_date: Optional[datetime] = None
    duration: Optional[int] = None 
    is_checked_in: Optional[bool] = None
    status: Optional[appointment_status_type] = None
    reason_for_visit: Optional[str] = None
    location: Optional[str] = None
    is_virtual: Optional[bool] = None
    details: Optional[str] = None
    patient_uid: Optional[uuid.UUID] = None 
    doctor_uid: Optional[uuid.UUID] = None

# response models
class AppointmentResponse(AppointmentBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }
    


#filter
class AppointmentFilter(BaseModel):
    start_date: Optional[datetime] = None
    duration: Optional[int] = None 
    is_checked_in: Optional[bool] = None
    status: Optional[appointment_status_type] = None
    reason_for_visit: Optional[str] = None
    location: Optional[str] = None
    is_virtual: Optional[bool] = None
    details: Optional[str] = None
    patient_uid: Optional[uuid.UUID] = None 
    doctor_uid: Optional[uuid.UUID] = None