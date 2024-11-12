from typing import List, Optional
from app.db.models import Admin
from app.db.main import db_session
from app.entities.admin.schema import AdminCreate, AdminUpdate, AdminResponse
from sqlmodel import select

class AdminRepo:

    async def get_all_admin(self, session: db_session) -> List[AdminResponse]:
        statement = select(Admin)
        result = await session.execute(statement)
        Admin = result.scalars().all()

        return [AdminResponse.model_validate(Admin) for Admin in Admin]
    
    async def get_admin(self, Admin_id: str, session: db_session) -> Optional[AdminResponse]:
        statement = select(Admin).where(Admin.uid == Admin_id)
        result = await session.execute(statement)
        Admin = result.scalars().one_or_none()

        return AdminResponse.model_validate(Admin) if Admin else None

    async def create_admin(self, Admin_data: AdminCreate, session: db_session) -> AdminResponse:
        new_Admin = Admin(**Admin_data.model_dump())
        session.add(new_Admin)
        await session.commit()
        await session.refresh(new_Admin)
        return AdminResponse.model_validate(new_Admin)
    
    async def update_admin(self, Admin_id: str, Admin: AdminUpdate, session: db_session) -> AdminResponse:
        statement = select(Admin).where(Admin.uid == Admin_id)
        result = await session.execute(statement)
        Admin_to_update = result.scalars().one_or_none()

        if not Admin_to_update:
            return None

        for key, value in Admin.model_dump(exclude_unset=True).items():
            setattr(Admin_to_update, key, value) 

        await session.commit()
        await session.refresh(Admin_to_update)
        return AdminResponse.model_validate(Admin_to_update)
    
    async def delete_admin(self, Admin_id: str, session: db_session) -> bool:
        statement = select(Admin).where(Admin.uid == Admin_id)
        result = await session.execute(statement)
        Admin_to_delete= result.scalars().one_or_none()
        if not Admin_to_delete:
            return False
        await session.delete(Admin_to_delete)
        await session.commit()
        return True
    
