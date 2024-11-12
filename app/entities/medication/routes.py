from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.medication.repo import MedicationRepo
from app.entities.medication.schema import MedicationResponse, MedicationCreate, MedicationUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Medication_router = APIRouter()
repo = MedicationRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Medication_router.get("/", response_model=List[MedicationResponse],
                          )
async def get_allmedication(session: db_session,   _details: access_token_bearer):
    return await MedicationRepo().get_allmedication(session)


@Medication_router.get("/{Medication_id}", response_model=MedicationResponse)
async def get_medication(Medication_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Medication =  await MedicationRepo().get_medication(Medication_id, session)
    if not Medication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medication not found")
    
    return Medication

@Medication_router.post("/", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
async def create_medication(Medication: MedicationCreate, session: db_session, _details: access_token_bearer):
    return await MedicationRepo().create_medication(Medication, session)


@Medication_router.put("/{Medication_id}", response_model=MedicationResponse)
async def update_medication(Medication_id: str, Medication: MedicationUpdate, session: db_session,  _details: access_token_bearer):    
    Medication = await MedicationRepo().get_medication(Medication_id, session)
    
    if not Medication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medication not found")
    return await MedicationRepo().update_medication(Medication_id, Medication, session)


@Medication_router.delete("/{Medication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medication(Medication_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await MedicationRepo().delete_medication(Medication_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medication not found")  
    return 
