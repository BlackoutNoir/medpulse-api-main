from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.appointment.repo import AppointmentRepo
from app.entities.appointment.schema import AppointmentResponse, AppointmentCreate, AppointmentUpdate, AppointmentFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
appointment_router = APIRouter()
repo = AppointmentRepo()

@appointment_router.get("/", response_model=List[AppointmentResponse], status_code=status.HTTP_200_OK)
async def get_all_Appointments(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_appointments(session)

@appointment_router.get("/{appointment_id}", response_model=AppointmentResponse, status_code=status.HTTP_200_OK)
async def get_appointment(appointment_id: str, session: db_session, user_details: access_token_bearer):
    appointment =  await repo.get_appointment(appointment_id, session)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appointment not found")
    
    return appointment


@appointment_router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_appointment(appointment, session)

@appointment_router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: str, updated_appointment: AppointmentUpdate, session: db_session,  user_details: access_token_bearer):    
    appointment = await repo.get_appointment(appointment_id, session)
    
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    return await repo.update_appointment(appointment_id, updated_appointment, session)


@appointment_router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_appointment(appointment_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")  
    return 

@appointment_router.post("/filtered-appointments", response_model=List[AppointmentResponse])
async def get_filtered_appointment(session: db_session, filters: AppointmentFilter):
    return await repo.filter_appointments(filters, session)
