from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class PagesBase(BaseModel):
    pass

class PagesCreate(PagesBase):
    pass

class PagesUpdate(PagesBase):
    pass


class PagesResponse(PagesBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }