from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.appointment.repo import AppointmentRepo
from app.entities.appointment.schema import AppointmentResponse, AppointmentCreate, AppointmentUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Appointment_router = APIRouter()
repo = AppointmentRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Appointment_router.get("/", response_model=List[AppointmentResponse],
                          )
async def get_allappointment(session: db_session,   _details: access_token_bearer):
    return await AppointmentRepo().get_allappointment(session)


@Appointment_router.get("/{Appointment_id}", response_model=AppointmentResponse)
async def get_appointment(Appointment_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Appointment =  await AppointmentRepo().get_appointment(Appointment_id, session)
    if not Appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    return Appointment

@Appointment_router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(Appointment: AppointmentCreate, session: db_session, _details: access_token_bearer):
    return await AppointmentRepo().create_appointment(Appointment, session)


@Appointment_router.put("/{Appointment_id}", response_model=AppointmentResponse)
async def update_appointment(Appointment_id: str, Appointment: AppointmentUpdate, session: db_session,  _details: access_token_bearer):    
    Appointment = await AppointmentRepo().get_appointment(Appointment_id, session)
    
    if not Appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return await AppointmentRepo().update_appointment(Appointment_id, Appointment, session)


@Appointment_router.delete("/{Appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(Appointment_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await AppointmentRepo().delete_appointment(Appointment_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")  
    return 
