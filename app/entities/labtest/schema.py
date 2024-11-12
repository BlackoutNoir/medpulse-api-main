from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class LabtestBase(BaseModel):
    pass

class LabtestCreate(LabtestBase):
    pass

class LabtestUpdate(LabtestBase):
    pass


class LabtestResponse(LabtestBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }