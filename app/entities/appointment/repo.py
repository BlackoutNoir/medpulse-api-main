from typing import List, Optional
from app.db.models import Appointment 
from app.db.main import db_session
from app.entities.appointment.schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentFilter
from sqlmodel import select, and_


class AppointmentRepo:

    async def get_all_appointments(self, session: db_session) -> List[AppointmentResponse]:
        statement = select(Appointment)
        result = await session.execute(statement)
        appointments = result.scalars().all()

        return [AppointmentResponse.model_validate(appointment) for appointment in appointments]
    
    async def get_appointment(self, appointment_id: str, session: db_session) -> Optional[AppointmentResponse]:
        statement = select(Appointment).where(Appointment.uid == appointment_id)
        result = await session.execute(statement)
        appointment = result.scalars().one_or_none()

        return AppointmentResponse.model_validate(appointment) if appointment else None
    
    async def create_appointment(self, appointment_data: AppointmentCreate, session: db_session) -> AppointmentResponse:
      
        new_appointment = Appointment(**appointment_data.model_dump())
        session.add(new_appointment)
        await session.commit()
        await session.refresh(new_appointment)

        return AppointmentResponse.model_validate(new_appointment)
    
    async def update_appointment(self, appointment_id: str, appointment: AppointmentUpdate, session: db_session) -> AppointmentResponse:
        statement = select(Appointment).where(Appointment.uid == appointment_id)
        result = await session.execute(statement)
        appointment_to_update = result.scalars().one_or_none()

        if not appointment_to_update:
            return None

        for key, value in appointment.model_dump(exclude_unset=True).items():
            setattr(appointment_to_update, key, value) 
            
        

        await session.commit()
        await session.refresh(appointment_to_update)
        return AppointmentResponse.model_validate(appointment_to_update)
    
    async def delete_appointment(self, appointment_id: str, session: db_session) -> bool:
        statement = select(Appointment).where(Appointment.uid == appointment_id)
        result = await session.execute(statement)
        appointment_to_delete= result.scalars().one_or_none()
        if not appointment_to_delete:
            return False
        await session.delete(appointment_to_delete)
        await session.commit()
        return True 
    

    async def filter_appointments(self, filters: AppointmentFilter, session: db_session) -> List[AppointmentResponse]:

        statement = select(Appointment)
        

        partial_match_fields = [
            "uuid","name","description"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(Appointment, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(Appointment, filters.order_by):
            order_column = getattr(Appointment, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        appointments = result.scalars().all()

        return [AppointmentResponse.model_validate(appointment) for appointment in appointments]