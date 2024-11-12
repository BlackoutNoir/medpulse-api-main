from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.prescription.repo import PrescriptionRepo
from app.entities.prescription.schema import PrescriptionResponse, PrescriptionCreate, PrescriptionUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Prescription_router = APIRouter()
repo = PrescriptionRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Prescription_router.get("/", response_model=List[PrescriptionResponse],
                          )
async def get_allprescription(session: db_session,   _details: access_token_bearer):
    return await PrescriptionRepo().get_allprescription(session)


@Prescription_router.get("/{Prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(Prescription_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Prescription =  await PrescriptionRepo().get_prescription(Prescription_id, session)
    if not Prescription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
    
    return Prescription

@Prescription_router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_prescription(Prescription: PrescriptionCreate, session: db_session, _details: access_token_bearer):
    return await PrescriptionRepo().create_prescription(Prescription, session)


@Prescription_router.put("/{Prescription_id}", response_model=PrescriptionResponse)
async def update_prescription(Prescription_id: str, Prescription: PrescriptionUpdate, session: db_session,  _details: access_token_bearer):    
    Prescription = await PrescriptionRepo().get_prescription(Prescription_id, session)
    
    if not Prescription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
    return await PrescriptionRepo().update_prescription(Prescription_id, Prescription, session)


@Prescription_router.delete("/{Prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription(Prescription_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await PrescriptionRepo().delete_prescription(Prescription_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")  
    return 
