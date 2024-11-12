from typing import List, Optional
from app.db.models import Diagnosis
from app.db.main import db_session
from app.entities.diagnosis.schema import DiagnosisCreate, DiagnosisUpdate, DiagnosisResponse
from sqlmodel import select

class DiagnosisRepo:

    async def get_all_diagnosis(self, session: db_session) -> List[DiagnosisResponse]:
        statement = select(Diagnosis)
        result = await session.execute(statement)
        Diagnosis = result.scalars().all()

        return [DiagnosisResponse.model_validate(diagnosis) for diagnosis in Diagnosis]
    
    async def get_diagnosis(self, Diagnosis_id: str, session: db_session) -> Optional[DiagnosisResponse]:
        statement = select(Diagnosis).where(Diagnosis.uid == Diagnosis_id)
        result = await session.execute(statement)
        diagnosis = result.scalars().one_or_none()

        return DiagnosisResponse.model_validate(diagnosis) if diagnosis else None

    async def create_diagnosis(self, diagnosis_data: DiagnosisCreate, session: db_session) -> DiagnosisResponse:
        new_diagnosis = Diagnosis(**diagnosis_data.model_dump())
        session.add(new_diagnosis)
        await session.commit()
        await session.refresh(new_diagnosis)
        return DiagnosisResponse.model_validate(new_diagnosis)
    
    async def update_diagnosis(self, Diagnosis_id: str, diagnosis: DiagnosisUpdate, session: db_session) -> DiagnosisResponse:
        statement = select(Diagnosis).where(Diagnosis.uid == Diagnosis_id)
        result = await session.execute(statement)
        diagnosis_to_update = result.scalars().one_or_none()

        if not diagnosis_to_update:
            return None

        for key, value in diagnosis.model_dump(exclude_unset=True).items():
            setattr(diagnosis_to_update, key, value) 

        await session.commit()
        await session.refresh(diagnosis_to_update)
        return DiagnosisResponse.model_validate(diagnosis_to_update)
    
    async def delete_diagnosis(self, Diagnosis_id: str, session: db_session) -> bool:
        statement = select(Diagnosis).where(Diagnosis.uid == Diagnosis_id)
        result = await session.execute(statement)
        diagnosis_to_delete= result.scalars().one_or_none()
        if not diagnosis_to_delete:
            return False
        await session.delete(diagnosis_to_delete)
        await session.commit()
        return True
    
