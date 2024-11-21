
from app.db.models import PageContent
from app.db.main import db_session
from app.entities.page.schema import PageContentCreate, PageContentUpdate
from typing import List
from sqlmodel import select
import uuid

class PageService:
    async def create_page_content(self, page_uid: uuid.UUID, session: db_session, content_data : PageContentCreate) -> None:

        new_content = PageContent(**content_data.model_dump())
        new_content.page_uid = page_uid
        session.add(new_content)
        await session.commit()
        await session.refresh(new_content)

    # async def update_page_content(self, content_id: str, content: PageContentUpdate, session: db_session) -> None:
    #     statement = select(PageContent).where(PageContent.uid == content_id)
    #     result = await session.execute(statement)
    #     content_to_update = result.scalars().one_or_none()

    #     if not content_to_update:
    #         return None

    #     for key, value in content.model_dump(exclude_unset=True).items():
    #         setattr(content_to_update, key, value) 

    #     await session.commit()
    #     await session.refresh(content_to_update)

    async def add_page_contents(self, page_uid : uuid.UUID , contents: List[PageContentUpdate], session: db_session) -> None:

        new_content = [content for content in contents if not content.uid]


        for content in new_content:
            await self.create_page_content(page_uid, session, content)

    async def delete_page_content(self, content_uid : uuid.UUID, session: db_session) -> None:
        statement = select(PageContent).where(PageContent.uid == content_uid)
        result = await session.execute(statement)
        content_to_delete= result.scalars().one_or_none()
        if content_to_delete:
            return
        await session.delete(content_to_delete)
        await session.commit()


    

        
                                 
    