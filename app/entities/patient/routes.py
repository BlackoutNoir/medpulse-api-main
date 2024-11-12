from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.patient.repo import PatientRepo
from app.entities.patient.schema import PatientResponse, PatientCreate, PatientUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Patient_router = APIRouter()
repo = PatientRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Patient_router.get("/", response_model=List[PatientResponse],
                          )
async def get_allpatient(session: db_session,   _details: access_token_bearer):
    return await PatientRepo().get_allpatient(session)


@Patient_router.get("/{Patient_id}", response_model=PatientResponse)
async def get_patient(Patient_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Patient =  await PatientRepo().get_patient(Patient_id, session)
    if not Patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    return Patient

@Patient_router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(Patient: PatientCreate, session: db_session, _details: access_token_bearer):
    return await PatientRepo().create_patient(Patient, session)


@Patient_router.put("/{Patient_id}", response_model=PatientResponse)
async def update_patient(Patient_id: str, Patient: PatientUpdate, session: db_session,  _details: access_token_bearer):    
    Patient = await PatientRepo().get_patient(Patient_id, session)
    
    if not Patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return await PatientRepo().update_patient(Patient_id, Patient, session)


@Patient_router.delete("/{Patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(Patient_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await PatientRepo().delete_patient(Patient_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")  
    return 
