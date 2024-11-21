from typing import List, Optional
from app.db.models import Patient, Insurance, MedicalHistory
from app.db.main import db_session
from app.entities.patient.schema import PatientCreate, PatientUpdate, PatientResponse, PatientFilter
from sqlmodel import select, and_


class PatientRepo:

    async def get_all_patients(self, session: db_session) -> List[PatientResponse]:
        statement = select(Patient)
        result = await session.execute(statement)
        patients = result.scalars().all()

        return [PatientResponse.model_validate(patient) for patient in patients]
    
    async def get_patient(self, patient_id: str, session: db_session) -> Optional[PatientResponse]:
        statement = select(Patient).where(Patient.uid == patient_id)
        result = await session.execute(statement)
        patient = result.scalars().one_or_none()

        return PatientResponse.model_validate(patient) if patient else None
    
    async def create_patient(self, patient_data: PatientCreate, session: db_session) -> PatientResponse:
        
        new_patient = Patient(**patient_data.model_dump())

        if patient_data.insurance:
            new_patient.insurance = [Insurance(**insurance_data.model_dump()) for insurance_data in patient_data.insurance]
        
        if patient_data.medical_history:
            new_patient.medical_history = [MedicalHistory(**medical_data.model_dump()) for medical_data in patient_data.medical_history]

        session.add(new_patient)
        await session.commit()
        await session.refresh(new_patient)

        return PatientResponse.model_validate(new_patient)
    
    async def update_patient(self, patient_id: str, patient: PatientUpdate, session: db_session) -> PatientResponse:
        statement = select(Patient).where(Patient.uid == patient_id)
        result = await session.execute(statement)
        patient_to_update = result.scalars().one_or_none()

        if not patient_to_update:
            return None

        for key, value in patient.model_dump(exclude_unset=True).items():
            if key == "insurance":
                patient_to_update.Insurance = [
                    Insurance(**insurance) if isinstance(insurance, dict) else insurance
                    for insurance in value
                ]
            else:
                setattr(patient_to_update, key, value)
        

        await session.commit()
        await session.refresh(patient_to_update)
        return PatientResponse.model_validate(patient_to_update)
    
    async def delete_patient(self, patient_id: str, session: db_session) -> bool:
        statement = select(Patient).where(Patient.uid == patient_id)
        result = await session.execute(statement)
        patient_to_delete= result.scalars().one_or_none()
        if not patient_to_delete:
            return False
        await session.delete(patient_to_delete)
        await session.commit()
        return True 
    

    async def filter_patients(self, filters: PatientFilter, session: db_session) -> List[PatientResponse]:

        statement = select(Patient)
        

        partial_match_fields = [
            "uuid","address"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(Patient, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(Patient, filters.order_by):
            order_column = getattr(Patient, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        patients = result.scalars().all()

        return [PatientResponse.model_validate(patient) for patient in patients]