from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.diagnosis.repo import DiagnosisRepo
from app.entities.diagnosis.schema import DiagnosisResponse, DiagnosisCreate, DiagnosisUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Diagnosis_router = APIRouter()
repo = DiagnosisRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Diagnosis_router.get("/", response_model=List[DiagnosisResponse],
                          )
async def get_allDiagnosis(session: db_session,   _details: access_token_bearer):
    return await DiagnosisRepo().get_allDiagnosis(session)


@Diagnosis_router.get("/{Diagnosis_id}", response_model=DiagnosisResponse)
async def get_diagnosis(Diagnosis_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Diagnosis =  await DiagnosisRepo().get_diagnosis(Diagnosis_id, session)
    if not Diagnosis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found")
    
    return Diagnosis

@Diagnosis_router.post("/", response_model=DiagnosisResponse, status_code=status.HTTP_201_CREATED)
async def create_diagnosis(diagnosis: DiagnosisCreate, session: db_session, _details: access_token_bearer):
    return await DiagnosisRepo().create_diagnosis(diagnosis, session)


@Diagnosis_router.put("/{Diagnosis_id}", response_model=DiagnosisResponse)
async def update_diagnosis(Diagnosis_id: str, diagnosis: DiagnosisUpdate, session: db_session,  _details: access_token_bearer):    
    Diagnosis = await DiagnosisRepo().get_diagnosis(Diagnosis_id, session)
    
    if not Diagnosis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found")
    return await DiagnosisRepo().update_diagnosis(Diagnosis_id, diagnosis, session)


@Diagnosis_router.delete("/{Diagnosis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diagnosis(Diagnosis_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await DiagnosisRepo().delete_diagnosis(Diagnosis_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found")  
    return 
