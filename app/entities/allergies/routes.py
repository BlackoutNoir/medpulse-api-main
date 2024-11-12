from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.allergies.repo import AllergiesRepo
from app.entities.allergies.schema import AllergiesResponse, AllergiesCreate, AllergiesUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Allergies_router = APIRouter()
repo = AllergiesRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Allergies_router.get("/", response_model=List[AllergiesResponse],
                          )
async def get_allallergies(session: db_session,   _details: access_token_bearer):
    return await AllergiesRepo().get_allallergies(session)


@Allergies_router.get("/{Allergies_id}", response_model=AllergiesResponse)
async def get_allergies(Allergies_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Allergies =  await AllergiesRepo().get_allergies(Allergies_id, session)
    if not Allergies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allergies not found")
    
    return Allergies

@Allergies_router.post("/", response_model=AllergiesResponse, status_code=status.HTTP_201_CREATED)
async def create_allergies(Allergies: AllergiesCreate, session: db_session, _details: access_token_bearer):
    return await AllergiesRepo().create_allergies(Allergies, session)


@Allergies_router.put("/{Allergies_id}", response_model=AllergiesResponse)
async def update_allergies(Allergies_id: str, Allergies: AllergiesUpdate, session: db_session,  _details: access_token_bearer):    
    Allergies = await AllergiesRepo().get_allergies(Allergies_id, session)
    
    if not Allergies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allergies not found")
    return await AllergiesRepo().update_allergies(Allergies_id, Allergies, session)


@Allergies_router.delete("/{Allergies_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_allergies(Allergies_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await AllergiesRepo().delete_Allergies(Allergies_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allergies not found")  
    return 
