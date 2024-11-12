from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class MedicationBase(BaseModel):
    pass

class MedicationCreate(MedicationBase):
    pass

class MedicationUpdate(MedicationBase):
    pass


class MedicationResponse(MedicationBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }