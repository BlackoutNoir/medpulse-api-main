from typing import List, Optional
from app.db.models import Labtest
from app.db.main import db_session
from app.entities.labtest.schema import LabtestCreate, LabtestUpdate, LabtestResponse
from sqlmodel import select

class LabtestRepo:

    async def get_all_labtest(self, session: db_session) -> List[LabtestResponse]:
        statement = select(Labtest)
        result = await session.execute(statement)
        Labtest = result.scalars().all()

        return [LabtestResponse.model_validate(Labtest) for Labtest in Labtest]
    
    async def get_labtest(self, Labtest_id: str, session: db_session) -> Optional[LabtestResponse]:
        statement = select(Labtest).where(Labtest.uid == Labtest_id)
        result = await session.execute(statement)
        Labtest = result.scalars().one_or_none()

        return LabtestResponse.model_validate(Labtest) if Labtest else None

    async def create_labtest(self, Labtest_data: LabtestCreate, session: db_session) -> LabtestResponse:
        new_Labtest = Labtest(**Labtest_data.model_dump())
        session.add(new_Labtest)
        await session.commit()
        await session.refresh(new_Labtest)
        return LabtestResponse.model_validate(new_Labtest)
    
    async def update_labtest(self, Labtest_id: str, Labtest: LabtestUpdate, session: db_session) -> LabtestResponse:
        statement = select(Labtest).where(Labtest.uid == Labtest_id)
        result = await session.execute(statement)
        Labtest_to_update = result.scalars().one_or_none()

        if not Labtest_to_update:
            return None

        for key, value in Labtest.model_dump(exclude_unset=True).items():
            setattr(Labtest_to_update, key, value) 

        await session.commit()
        await session.refresh(Labtest_to_update)
        return LabtestResponse.model_validate(Labtest_to_update)
    
    async def delete_labtest(self, Labtest_id: str, session: db_session) -> bool:
        statement = select(Labtest).where(Labtest.uid == Labtest_id)
        result = await session.execute(statement)
        Labtest_to_delete= result.scalars().one_or_none()
        if not Labtest_to_delete:
            return False
        await session.delete(Labtest_to_delete)
        await session.commit()
        return True
    
