from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class AppointmentBase(BaseModel):
    pass

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }