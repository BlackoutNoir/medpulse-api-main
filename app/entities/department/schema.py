from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class DepartmentBase(BaseModel):
    pass

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }