from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class DiagnosisBase(BaseModel):
    pass

class DiagnosisCreate(DiagnosisBase):
    pass

class DiagnosisUpdate(DiagnosisBase):
    pass


class DiagnosisResponse(DiagnosisBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }