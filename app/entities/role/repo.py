from typing import List, Optional
from app.db.models import Role, Permission
from app.db.main import db_session
from app.entities.role.schema import RoleResponse, RoleCreate, RoleUpdate, RoleFilter, PermissionResponse
from sqlmodel import select, and_


class RoleRepo:

    async def get_all_roles(self, session: db_session) -> List[RoleResponse]:
        statement = select(Role)
        result = await session.execute(statement)
        roles = result.scalars().all()

        return [RoleResponse.model_validate(role) for role in roles]
    
    async def get_role(self, role_id: str, session: db_session) -> Optional[RoleResponse]:
        statement = select(Role).where(Role.uid == role_id)
        result = await session.execute(statement)
        role = result.scalars().one_or_none()

        return RoleResponse.model_validate(role) if role else None
    
    async def create_role(self, role_data: RoleCreate, session: db_session) -> RoleResponse:
      
        new_role = Role(**role_data.model_dump())
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)

        return RoleResponse.model_validate(new_role)
    
    async def update_role(self, role_id: str, role: RoleUpdate, session: db_session) -> RoleResponse:
        statement = select(Role).where(Role.uid == role_id)
        result = await session.execute(statement)
        role_to_update = result.scalars().one_or_none()

        if not role_to_update:
            return None

        for key, value in role.model_dump(exclude_unset=True).items():
            setattr(role_to_update, key, value) 
        
        await session.commit()
        await session.refresh(role_to_update)
        return RoleResponse.model_validate(role_to_update)
    
    async def delete_role(self, role_id: str, session: db_session) -> bool:
        statement = select(Role).where(Role.uid == role_id)
        result = await session.execute(statement)
        role_to_delete= result.scalars().one_or_none()
        if not role_to_delete:
            return False
        await session.delete(role_to_delete)
        await session.commit()
        return True 
    

    async def filter_roles(self, filters: RoleFilter, session: db_session) -> List[RoleResponse]:

        statement = select(Role)
        

        partial_match_fields = [
            "description"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            column = getattr(Role, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        result = await session.execute(statement)
        roles = result.scalars().all()

        return [RoleResponse.model_validate(role) for role in roles]
    

    async def get_permissions(self, session: db_session) -> List[PermissionResponse]:
        statement = select(Permission)
        result = await session.execute(statement)
        permissions = result.scalars().all()

        return [PermissionResponse.model_validate(p) for p in permissions]
    

    