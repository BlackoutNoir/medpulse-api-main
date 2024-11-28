from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

# Base models

class PageBase(BaseModel):
    title: str
    created_by: str
    is_visible: bool = True

class PageContentBase(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    paragraph: Optional[str] = None
    image_url: Optional[str] = None


# Create models

class PageCreate(PageBase):
    contents : List["PageContentCreate"]

class PageContentCreate(PageContentBase):
    page_id: uuid.UUID  


# Update models

class PageUpdate(PageBase):
    title: Optional[str] = None
    created_by: Optional[str] = None
    is_visible: Optional[bool] = None
    contents : List["PageContentUpdate"]

class PageContentUpdate(PageContentBase):
    uid: Optional[uuid.UUID]  = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    paragraph: Optional[str] = None
    image_url: Optional[str] = None


# Response models

class PageContentResponse(PageContentBase):
    uid: uuid.UUID 

    model_config = {
        "from_attributes": True
    }

class PageResponse(PageBase):
    uid: uuid.UUID  
    created_date: datetime
    last_modified: datetime
    contents: List[PageContentResponse] 

    model_config = {
        "from_attributes": True
    }


# Filter models

class PageFilter(PageBase):
    title: Optional[str] = None
    created_by: Optional[str] = None
    is_visible: Optional[bool] = None
    created_date: Optional[datetime] = None
    order_by: Optional[str] = None 

