from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class PrescriptionBase(BaseModel):
    pass

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(PrescriptionBase):
    pass


class PrescriptionResponse(PrescriptionBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }