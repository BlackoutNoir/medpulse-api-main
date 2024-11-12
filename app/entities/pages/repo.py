from typing import List, Optional
from app.db.models import Pages
from app.db.main import db_session
from app.entities.pages.schema import PagesCreate, PagesUpdate, PagesResponse
from sqlmodel import select

class PagesRepo:

    async def get_all_pages(self, session: db_session) -> List[PagesResponse]:
        statement = select(Pages)
        result = await session.execute(statement)
        Pages = result.scalars().all()

        return [PagesResponse.model_validate(Pages) for Pages in Pages]
    
    async def get_pages(self, Pages_id: str, session: db_session) -> Optional[PagesResponse]:
        statement = select(Pages).where(Pages.uid == Pages_id)
        result = await session.execute(statement)
        Pages = result.scalars().one_or_none()

        return PagesResponse.model_validate(Pages) if Pages else None

    async def create_pages(self, Pages_data: PagesCreate, session: db_session) -> PagesResponse:
        new_Pages = Pages(**Pages_data.model_dump())
        session.add(new_Pages)
        await session.commit()
        await session.refresh(new_Pages)
        return PagesResponse.model_validate(new_Pages)
    
    async def update_pages(self, Pages_id: str, Pages: PagesUpdate, session: db_session) -> PagesResponse:
        statement = select(Pages).where(Pages.uid == Pages_id)
        result = await session.execute(statement)
        Pages_to_update = result.scalars().one_or_none()

        if not Pages_to_update:
            return None

        for key, value in Pages.model_dump(exclude_unset=True).items():
            setattr(Pages_to_update, key, value) 

        await session.commit()
        await session.refresh(Pages_to_update)
        return PagesResponse.model_validate(Pages_to_update)
    
    async def delete_pages(self, Pages_id: str, session: db_session) -> bool:
        statement = select(Pages).where(Pages.uid == Pages_id)
        result = await session.execute(statement)
        Pages_to_delete= result.scalars().one_or_none()
        if not Pages_to_delete:
            return False
        await session.delete(Pages_to_delete)
        await session.commit()
        return True
    
