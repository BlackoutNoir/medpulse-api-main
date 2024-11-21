from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.doctor.repo import DoctorRepo
from app.entities.doctor.schema import DoctorResponse, DoctorCreate, DoctorUpdate, DoctorFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
doctor_router = APIRouter()
repo = DoctorRepo()

@doctor_router.get("/", response_model=List[DoctorResponse], status_code=status.HTTP_200_OK)
async def get_all_Doctors(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_doctors(session)

@doctor_router.get("/{doctor_id}", response_model=DoctorResponse, status_code=status.HTTP_200_OK)
async def get_doctor(doctor_id: str, session: db_session, user_details: access_token_bearer):
    doctor =  await repo.get_doctor(doctor_id, session)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="doctor not found")
    
    return doctor


@doctor_router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: DoctorCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_doctor(doctor, session)

@doctor_router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(doctor_id: str, updated_doctor: DoctorUpdate, session: db_session,  user_details: access_token_bearer):    
    doctor = await repo.get_doctor(doctor_id, session)
    
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    return await repo.update_doctor(doctor_id, updated_doctor, session)


@doctor_router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_doctor(doctor_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")  
    return 

@doctor_router.post("/filtered-doctors", response_model=List[DoctorResponse])
async def get_filtered_doctor(session: db_session, filters: DoctorFilter):
    return await repo.filter_doctors(filters, session)
