from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class BillBase(BaseModel):
    pass

class BillCreate(BillBase):
    pass

class BillUpdate(BillBase):
    pass


class BillResponse(BillBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }