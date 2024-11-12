from typing import List, Optional
from app.db.models import Allergies
from app.db.main import db_session
from app.entities.allergies.schema import AllergiesCreate, AllergiesUpdate, AllergiesResponse
from sqlmodel import select

class AllergiesRepo:

    async def get_all_allergies(self, session: db_session) -> List[AllergiesResponse]:
        statement = select(Allergies)
        result = await session.execute(statement)
        Allergies = result.scalars().all()

        return [AllergiesResponse.model_validate(Allergies) for Allergies in Allergies]
    
    async def get_allergies(self, Allergies_id: str, session: db_session) -> Optional[AllergiesResponse]:
        statement = select(Allergies).where(Allergies.uid == Allergies_id)
        result = await session.execute(statement)
        Allergies = result.scalars().one_or_none()

        return AllergiesResponse.model_validate(Allergies) if Allergies else None

    async def create_allergies(self, Allergies_data: AllergiesCreate, session: db_session) -> AllergiesResponse:
        new_Allergies = Allergies(**Allergies_data.model_dump())
        session.add(new_Allergies)
        await session.commit()
        await session.refresh(new_Allergies)
        return AllergiesResponse.model_validate(new_Allergies)
    
    async def update_allergies(self, Allergies_id: str, Allergies: AllergiesUpdate, session: db_session) -> AllergiesResponse:
        statement = select(Allergies).where(Allergies.uid == Allergies_id)
        result = await session.execute(statement)
        Allergies_to_update = result.scalars().one_or_none()

        if not Allergies_to_update:
            return None

        for key, value in Allergies.model_dump(exclude_unset=True).items():
            setattr(Allergies_to_update, key, value) 

        await session.commit()
        await session.refresh(Allergies_to_update)
        return AllergiesResponse.model_validate(Allergies_to_update)
    
    async def delete_allergies(self, Allergies_id: str, session: db_session) -> bool:
        statement = select(Allergies).where(Allergies.uid == Allergies_id)
        result = await session.execute(statement)
        Allergies_to_delete= result.scalars().one_or_none()
        if not Allergies_to_delete:
            return False
        await session.delete(Allergies_to_delete)
        await session.commit()
        return True
    
