from typing import List, Optional
from app.db.models import Patient
from app.db.main import db_session
from app.entities.patient.schema import PatientCreate, PatientUpdate, PatientResponse
from sqlmodel import select

class PatientRepo:

    async def get_all_patient(self, session: db_session) -> List[PatientResponse]:
        statement = select(Patient)
        result = await session.execute(statement)
        Patient = result.scalars().all()

        return [PatientResponse.model_validate(Patient) for Patient in Patient]
    
    async def get_patient(self, Patient_id: str, session: db_session) -> Optional[PatientResponse]:
        statement = select(Patient).where(Patient.uid == Patient_id)
        result = await session.execute(statement)
        Patient = result.scalars().one_or_none()

        return PatientResponse.model_validate(Patient) if Patient else None

    async def create_patient(self, Patient_data: PatientCreate, session: db_session) -> PatientResponse:
        new_Patient = Patient(**Patient_data.model_dump())
        session.add(new_Patient)
        await session.commit()
        await session.refresh(new_Patient)
        return PatientResponse.model_validate(new_Patient)
    
    async def update_patient(self, Patient_id: str, Patient: PatientUpdate, session: db_session) -> PatientResponse:
        statement = select(Patient).where(Patient.uid == Patient_id)
        result = await session.execute(statement)
        Patient_to_update = result.scalars().one_or_none()

        if not Patient_to_update:
            return None

        for key, value in Patient.model_dump(exclude_unset=True).items():
            setattr(Patient_to_update, key, value) 

        await session.commit()
        await session.refresh(Patient_to_update)
        return PatientResponse.model_validate(Patient_to_update)
    
    async def delete_patient(self, Patient_id: str, session: db_session) -> bool:
        statement = select(Patient).where(Patient.uid == Patient_id)
        result = await session.execute(statement)
        Patient_to_delete= result.scalars().one_or_none()
        if not Patient_to_delete:
            return False
        await session.delete(Patient_to_delete)
        await session.commit()
        return True
    
