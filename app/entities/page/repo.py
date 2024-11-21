from typing import List, Optional
from app.db.models import Page, PageContent
from app.db.main import db_session
from app.entities.page.schema import PageCreate, PageUpdate, PageResponse, PageFilter
from sqlmodel import select, and_
from app.entities.page.service import PageService

page_service = PageService()

class PageRepo:

    async def get_all_pages(self, session: db_session) -> List[PageResponse]:
        statement = select(Page)
        result = await session.execute(statement)
        pages = result.scalars().all()

        return [PageResponse.model_validate(page) for page in pages]
    
    async def get_page(self, Page_id: str, session: db_session) -> Optional[PageResponse]:
        statement = select(Page).where(Page.uid == Page_id)
        result = await session.execute(statement)
        page = result.scalars().one_or_none()

        return PageResponse.model_validate(page) if page else None

    async def create_page(self, Page_data: PageCreate, session: db_session) -> PageResponse:
        new_page = Page(**Page_data.model_dump(exclude={"contents"}))
        

        # for content_data in Page_data.contents:
        #     page_service.create_page_content(new_Page.uid, content_data, session)

        if Page_data.contents:
            new_page.contents = [PageContent(**content_data.model_dump()) for content_data in Page_data.contents]
        
        session.add(new_page)   
        await session.commit()
        await session.refresh(new_page)
        return PageResponse.model_validate(new_page)
    
    async def update_page(self, page_id: str, page: PageUpdate, session: db_session) -> PageResponse:
        statement = select(Page).where(Page.uid == page_id)
        result = await session.execute(statement)
        page_to_update = result.scalars().one_or_none()

        if not page_to_update:
            return None

        for key, value in page.model_dump(exclude_unset=True).items():
            if key == "contents":
                # Convert each item to a PageContent instance
                page_to_update.contents = [
                    PageContent(**content_data) if isinstance(content_data, dict) else content_data
                    for content_data in value
                ]
            else:
                setattr(page_to_update, key, value)

        # removed_content = {content.uid for content in page_to_update.contents if content.uid not in [c.uid for c in page.contents]}

        # for content in removed_content:
        #     await page_service.delete_page_content(content, session)

        # await page_service.add_page_contents(page_to_update.uid, page.contents, session)

        await session.commit()
        await session.refresh(page_to_update)
        return PageResponse.model_validate(page_to_update)
    
    async def delete_page(self, page_id: str, session: db_session) -> bool:
        statement = select(Page).where(Page.uid == page_id)
        result = await session.execute(statement)
        page_to_delete= result.scalars().one_or_none()
        if not page_to_delete: 
            return False
        await session.delete(page_to_delete)
        await session.commit()
        return True
    
    async def filter_pages(self, filters: PageFilter, session: db_session) -> List[PageResponse]:

        statement = select(Page)
        

        partial_match_fields = [
            "uuid","title","subtitle","paragraph"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(Page, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(Page, filters.order_by):
            order_column = getattr(Page, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        pages = result.scalars().all()

        return [PageResponse.model_validate(page) for page in pages]
