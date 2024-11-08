from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class LogBase(BaseModel):
    pass

class LogCreate(LogBase):
    pass

class LogUpdate(LogBase):
    pass


class LogResponse(LogBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }