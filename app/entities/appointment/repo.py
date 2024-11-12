from typing import List, Optional
from app.db.models import Appointment
from app.db.main import db_session
from app.entities.appointment.schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from sqlmodel import select

class AppointmentRepo:

    async def get_all_appointment(self, session: db_session) -> List[AppointmentResponse]:
        statement = select(Appointment)
        result = await session.execute(statement)
        Appointment = result.scalars().all()

        return [AppointmentResponse.model_validate(Appointment) for Appointment in Appointment]
    
    async def get_appointment(self, Appointment_id: str, session: db_session) -> Optional[AppointmentResponse]:
        statement = select(Appointment).where(Appointment.uid == Appointment_id)
        result = await session.execute(statement)
        Appointment = result.scalars().one_or_none()

        return AppointmentResponse.model_validate(Appointment) if Appointment else None

    async def create_appointment(self, Appointment_data: AppointmentCreate, session: db_session) -> AppointmentResponse:
        new_Appointment = Appointment(**Appointment_data.model_dump())
        session.add(new_Appointment)
        await session.commit()
        await session.refresh(new_Appointment)
        return AppointmentResponse.model_validate(new_Appointment)
    
    async def update_appointment(self, Appointment_id: str, Appointment: AppointmentUpdate, session: db_session) -> AppointmentResponse:
        statement = select(Appointment).where(Appointment.uid == Appointment_id)
        result = await session.execute(statement)
        Appointment_to_update = result.scalars().one_or_none()

        if not Appointment_to_update:
            return None

        for key, value in Appointment.model_dump(exclude_unset=True).items():
            setattr(Appointment_to_update, key, value) 

        await session.commit()
        await session.refresh(Appointment_to_update)
        return AppointmentResponse.model_validate(Appointment_to_update)
    
    async def delete_appointment(self, Appointment_id: str, session: db_session) -> bool:
        statement = select(Appointment).where(Appointment.uid == Appointment_id)
        result = await session.execute(statement)
        Appointment_to_delete= result.scalars().one_or_none()
        if not Appointment_to_delete:
            return False
        await session.delete(Appointment_to_delete)
        await session.commit()
        return True
    
