from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.patient.repo import PatientRepo
from app.entities.patient.schema import PatientResponse, PatientCreate, PatientUpdate, PatientFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


patient_router = APIRouter()
repo = PatientRepo()

@patient_router.get("/", response_model=List[PatientResponse], status_code=status.HTTP_200_OK)
async def get_all_Patients(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_patients(session)

@patient_router.get("/{patient_id}", response_model=PatientResponse, status_code=status.HTTP_200_OK)
async def get_patient(patient_id: str, session: db_session, user_details: access_token_bearer):
    patient =  await repo.get_patient(patient_id, session)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="patient not found")
    
    return patient


@patient_router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_patient(patient, session)

@patient_router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: str, updated_patient: PatientUpdate, session: db_session,  user_details: access_token_bearer):    
    patient = await repo.get_patient(patient_id, session)
    
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    return await repo.update_patient(patient_id, updated_patient, session)


@patient_router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_patient(patient_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")  
    return 

@patient_router.post("/filtered-patients", response_model=List[PatientResponse])
async def get_filtered_patient(session: db_session, filters: PatientFilter):
    return await repo.filter_patients(filters, session)
