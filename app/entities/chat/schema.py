from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid



class ChatBase(BaseModel):
    pass

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    pass


class ChatResponse(ChatBase):
    uid: uuid.UUID

    model_config = {
        "from_attributes": True
    }