from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class PatientBase(BaseModel):
    pass

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass


class PatientResponse(PatientBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }