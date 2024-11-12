from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.bill.repo import BillRepo
from app.entities.bill.schema import BillResponse, BillCreate, BillUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Bill_router = APIRouter()
repo = BillRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Bill_router.get("/", response_model=List[BillResponse],
                          )
async def get_allbill(session: db_session,   _details: access_token_bearer):
    return await BillRepo().get_allbill(session)


@Bill_router.get("/{Bill_id}", response_model=BillResponse)
async def get_bill(Bill_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Bill =  await BillRepo().get_bill(Bill_id, session)
    if not Bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
    
    return Bill

@Bill_router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
async def create_bill(Bill: BillCreate, session: db_session, _details: access_token_bearer):
    return await BillRepo().create_bill(Bill, session)


@Bill_router.put("/{Bill_id}", response_model=BillResponse)
async def update_bill(Bill_id: str, Bill: BillUpdate, session: db_session,  _details: access_token_bearer):    
    Bill = await BillRepo().get_bill(Bill_id, session)
    
    if not Bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
    return await BillRepo().update_bill(Bill_id, Bill, session)


@Bill_router.delete("/{Bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bill(Bill_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await BillRepo().delete_bill(Bill_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")  
    return 
