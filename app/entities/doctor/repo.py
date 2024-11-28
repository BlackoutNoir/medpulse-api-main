from typing import List, Optional
from app.db.models import Doctor 
from app.db.main import db_session
from app.entities.doctor.schema import DoctorCreate, DoctorUpdate, DoctorResponse, DoctorFilter
from sqlmodel import select, and_


class DoctorRepo:

    async def get_all_doctors(self, session: db_session) -> List[DoctorResponse]:
        statement = select(Doctor)
        result = await session.execute(statement)
        doctors = result.scalars().all()

        return [DoctorResponse.model_validate(doctor) for doctor in doctors]
    
    async def get_doctor(self, doctor_id: str, session: db_session) -> Optional[DoctorResponse]:
        statement = select(Doctor).where(Doctor.uid == doctor_id)
        result = await session.execute(statement)
        doctor = result.scalars().one_or_none()

        return DoctorResponse.model_validate(doctor) if doctor else None
    
    async def create_doctor(self, doctor_data: DoctorCreate, session: db_session) -> DoctorResponse:
      
        new_doctor = Doctor(**doctor_data.model_dump())
        session.add(new_doctor)
        await session.commit()
        await session.refresh(new_doctor)

        return DoctorResponse.model_validate(new_doctor)
    
    async def update_doctor(self, doctor_id: str, doctor: DoctorUpdate, session: db_session) -> DoctorResponse:
        statement = select(Doctor).where(Doctor.uid == doctor_id)
        result = await session.execute(statement)
        doctor_to_update = result.scalars().one_or_none()

        if not doctor_to_update:
            return None

        for key, value in doctor.model_dump(exclude_unset=True).items():
            setattr(doctor_to_update, key, value) 
            
        

        await session.commit()
        await session.refresh(doctor_to_update)
        return DoctorResponse.model_validate(doctor_to_update)
    
    async def delete_doctor(self, doctor_id: str, session: db_session) -> bool:
        statement = select(Doctor).where(Doctor.uid == doctor_id)
        result = await session.execute(statement)
        doctor_to_delete= result.scalars().one_or_none()
        if not doctor_to_delete:
            return False
        await session.delete(doctor_to_delete)
        await session.commit()
        return True 
    

    async def filter_doctors(self, filters: DoctorFilter, session: db_session) -> List[DoctorResponse]:

        statement = select(Doctor)
        

        partial_match_fields = [
            "uuid","name"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(Doctor, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(Doctor, filters.order_by):
            order_column = getattr(Doctor, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        doctors = result.scalars().all()

        return [DoctorResponse.model_validate(doctor) for doctor in doctors]