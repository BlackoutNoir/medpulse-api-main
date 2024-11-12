from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class AdminBase(BaseModel):
    pass

class AdminCreate(AdminBase):
    pass

class AdminUpdate(AdminBase):
    pass


class AdminResponse(AdminBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }