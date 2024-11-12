from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class AllergiesBase(BaseModel):
    pass

class AllergiesCreate(AllergiesBase):
    pass

class AllergiesUpdate(AllergiesBase):
    pass


class AllergiesResponse(AllergiesBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }