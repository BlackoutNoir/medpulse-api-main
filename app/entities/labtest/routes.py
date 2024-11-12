from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.labtest.repo import LabtestRepo
from app.entities.labtest.schema import LabtestResponse, LabtestCreate, LabtestUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Labtest_router = APIRouter()
repo = LabtestRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Labtest_router.get("/", response_model=List[LabtestResponse],
                          )
async def get_alllabtest(session: db_session,   _details: access_token_bearer):
    return await LabtestRepo().get_alllabtest(session)


@Labtest_router.get("/{Labtest_id}", response_model=LabtestResponse)
async def get_labtest(Labtest_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Labtest =  await LabtestRepo().get_labtest(Labtest_id, session)
    if not Labtest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Labtest not found")
    
    return Labtest

@Labtest_router.post("/", response_model=LabtestResponse, status_code=status.HTTP_201_CREATED)
async def create_labtest(Labtest: LabtestCreate, session: db_session, _details: access_token_bearer):
    return await LabtestRepo().create_labtest(Labtest, session)


@Labtest_router.put("/{Labtest_id}", response_model=LabtestResponse)
async def update_labtest(Labtest_id: str, Labtest: LabtestUpdate, session: db_session,  _details: access_token_bearer):    
    Labtest = await LabtestRepo().get_labtest(Labtest_id, session)
    
    if not Labtest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Labtest not found")
    return await LabtestRepo().update_labtest(Labtest_id, Labtest, session)


@Labtest_router.delete("/{Labtest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_labtest(Labtest_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await LabtestRepo().delete_labtest(Labtest_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Labtest not found")  
    return 
