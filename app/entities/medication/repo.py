from typing import List, Optional
from app.db.models import Medication
from app.db.main import db_session
from app.entities.medication.schema import MedicationCreate, MedicationUpdate, MedicationResponse
from sqlmodel import select

class MedicationRepo:

    async def get_all_medication(self, session: db_session) -> List[MedicationResponse]:
        statement = select(Medication)
        result = await session.execute(statement)
        Medication = result.scalars().all()

        return [MedicationResponse.model_validate(Medication) for Medication in Medication]
    
    async def get_medication(self, Medication_id: str, session: db_session) -> Optional[MedicationResponse]:
        statement = select(Medication).where(Medication.uid == Medication_id)
        result = await session.execute(statement)
        Medication = result.scalars().one_or_none()

        return MedicationResponse.model_validate(Medication) if Medication else None

    async def create_medication(self, Medication_data: MedicationCreate, session: db_session) -> MedicationResponse:
        new_Medication = Medication(**Medication_data.model_dump())
        session.add(new_Medication)
        await session.commit()
        await session.refresh(new_Medication)
        return MedicationResponse.model_validate(new_Medication)
    
    async def update_medication(self, Medication_id: str, Medication: MedicationUpdate, session: db_session) -> MedicationResponse:
        statement = select(Medication).where(Medication.uid == Medication_id)
        result = await session.execute(statement)
        Medication_to_update = result.scalars().one_or_none()

        if not Medication_to_update:
            return None

        for key, value in Medication.model_dump(exclude_unset=True).items():
            setattr(Medication_to_update, key, value) 

        await session.commit()
        await session.refresh(Medication_to_update)
        return MedicationResponse.model_validate(Medication_to_update)
    
    async def delete_medication(self, Medication_id: str, session: db_session) -> bool:
        statement = select(Medication).where(Medication.uid == Medication_id)
        result = await session.execute(statement)
        Medication_to_delete= result.scalars().one_or_none()
        if not Medication_to_delete:
            return False
        await session.delete(Medication_to_delete)
        await session.commit()
        return True
    
