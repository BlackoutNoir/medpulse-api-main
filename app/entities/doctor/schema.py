from pydantic import BaseModel
from typing import Optional, List
import uuid


# Base models
class DoctorBase(BaseModel):
    staff_uid: uuid.UUID
    specializations: List[str]
    qualifications: List[str]
    years_of_experience: int
    enable_online_appointments : bool


# creation model
class DoctorCreate(DoctorBase):
    pass


# update model
class DoctorUpdate(DoctorBase):
    staff_uid: Optional[uuid.UUID] = None
    specializations: Optional[List[str]] = None
    qualifications: Optional[List[str]] = None
    years_of_experience: Optional[int] = None
    enable_online_appointments: Optional[bool] = None

# response models
class DoctorResponse(DoctorBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }


#filter
class DoctorFilter(BaseModel):
    uid : Optional[uuid.UUID] = None
    staff_uid: Optional[uuid.UUID] = None
    specializations: Optional[List[str]] = None
    qualifications: Optional[List[str]] = None
    years_of_experience: Optional[int] = None
    enable_online_appointments: Optional[bool] = None
    order_by: Optional[str] = None