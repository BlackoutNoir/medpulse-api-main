from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class StaffBase(BaseModel):
    pass

class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass


class StaffResponse(StaffBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }