from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.page.repo import PageRepo
from app.entities.page.schema import PageResponse, PageCreate, PageUpdate, PageFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
page_router = APIRouter()
repo = PageRepo()

@page_router.get("/", response_model=List[PageResponse], status_code=status.HTTP_200_OK)
async def get_all_pages(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_pages(session)

@page_router.get("/{page_id}", response_model=PageResponse, status_code=status.HTTP_200_OK)
async def get_page(page_id: str, session: db_session, user_details: access_token_bearer):
    page =  await repo.get_page(page_id, session)
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="page not found")
    
    return page


@page_router.post("/", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(page: PageCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_page(page, session)

@page_router.put("/{page_id}", response_model=PageResponse)
async def update_page(page_id: str, updated_page : PageUpdate, session: db_session,  user_details: access_token_bearer):    
    page = await repo.get_page(page_id, session)
    
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    
    return await repo.update_page(page_id, updated_page, session)


@page_router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(page_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_page(page_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")  
    return 

@page_router.post("/filtered-pages", response_model=List[PageResponse])
async def get_filtered_pages(session: db_session, filters: PageFilter):
    return await repo.filter_pages(filters, session)