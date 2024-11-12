from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.pages.repo import PagesRepo
from app.entities.pages.schema import PagesResponse, PagesCreate, PagesUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Pages_router = APIRouter()
repo = PagesRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Pages_router.get("/", response_model=List[PagesResponse],
                          )
async def get_allpages(session: db_session,   _details: access_token_bearer):
    return await PagesRepo().get_allpages(session)


@Pages_router.get("/{Pages_id}", response_model=PagesResponse)
async def get_pages(Pages_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Pages =  await PagesRepo().get_pages(Pages_id, session)
    if not Pages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pages not found")
    
    return Pages

@Pages_router.post("/", response_model=PagesResponse, status_code=status.HTTP_201_CREATED)
async def create_pages(Pages: PagesCreate, session: db_session, _details: access_token_bearer):
    return await PagesRepo().create_pages(Pages, session)


@Pages_router.put("/{Pages_id}", response_model=PagesResponse)
async def update_pages(Pages_id: str, Pages: PagesUpdate, session: db_session,  _details: access_token_bearer):    
    Pages = await PagesRepo().get_pages(Pages_id, session)
    
    if not Pages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pages not found")
    return await PagesRepo().update_pages(Pages_id, Pages, session)


@Pages_router.delete("/{Pages_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pages(Pages_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await PagesRepo().delete_pages(Pages_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pages not found")  
    return 
