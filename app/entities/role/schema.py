from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid



# class Role(SQLModel, table=True):
    # __tablename__ = 'role'

    # uid: uuid.UUID = Field(
    #     sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    # )

    # name: str = Field(unique=True, nullable=False)
    # description: Optional[str] = None

    # staff: List["Staff"] = Relationship(back_populates="role")

    # permissions: List["Permission"] = Relationship(
    #     back_populates="roles",
    #     link_model=RolePermission,
    #     sa_relationship_kwargs={"lazy": "selectin"}
    # )
# Base model
class RoleBase(BaseModel):
    name: str
    description: str

class PermissionBase(BaseModel):
    uid: uuid.UUID

# Create model
class RoleCreate(RoleBase):
    permissions: List[PermissionBase]

class PermissionBase(BaseModel):
    uid: uuid.UUID


# Update model
class RoleUpdate(RoleBase):
    name:str
    description:str
    permissions: List[PermissionBase]




# Response model

class PermissionResponse(PermissionBase):
    uid : uuid.UUID
    description : str

    model_config = {
        "from_attributes": True
    }

class RoleResponse(RoleBase):
    uid: uuid.UUID
    permissions: List[PermissionResponse]

    model_config = {
        "from_attributes": True
    }

# Filter model
class RoleFilter(RoleBase):
    name: Optional[str] = None
    description: Optional[str] = None
    order_by: Optional[str] = None


