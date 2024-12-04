from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import date, datetime
from app.entities.user.schema import UserNested



# Base models
class StaffBase(BaseModel):
    user_uid: uuid.UUID
    employment_date: date = date.today
    employed_until: Optional[date] = None
    employment_type: str
    role_uid: uuid.UUID 
    department_uid: uuid.UUID 


class ScheduleBase(BaseModel):
    uid: uuid.UUID 
    shift_start: datetime
    shift_end: datetime
    day_of_week: str  
    location: Optional[str]  
    notes: Optional[str] 

# creation model
class ScheduleCreate(ScheduleBase):
    staff_id: uuid.UUID

class StaffCreate(StaffBase):
    schedules: List[ScheduleCreate]
    pass


# update model
class ScheduleUpdate(ScheduleBase):
    staff_id: uuid.UUID

class StaffUpdate(StaffBase):
    user_uid: Optional[uuid.UUID]= None
    employment_date: Optional[date] = None
    employed_until: Optional[date] = None
    role_uid: Optional[uuid.UUID] = None
    department_uid: Optional[uuid.UUID] = None
    schedules: Optional[List[ScheduleUpdate]] = None


# response models

class ScheduleResponse(ScheduleBase):
    
    model_config = {
        "from_attributes": True
    }


class StaffResponse(StaffBase):
    uid: uuid.UUID

    schedules = List[ScheduleResponse]

    user: UserNested

    model_config = {
        "from_attributes": True
    }


#filter
class StaffFilter(BaseModel):
    uid : Optional[uuid.UUID] = None
    user_uid: Optional[uuid.UUID]= None
    employment_date: Optional[date] = None
    employed_until: Optional[date] = None
    role_uid: Optional[uuid.UUID] = None
    department_uid: Optional[uuid.UUID] = None
    order_by: Optional[str] = None

#export
class StaffNested(StaffBase):

    uid: uuid.UUID
    schedules = List[ScheduleResponse]
    user: UserNested
    model_config = {
        "from_attributes": True
    }