from typing import List, Optional
from app.db.models import Prescription
from app.db.main import db_session
from app.entities.prescription.schema import PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse
from sqlmodel import select

class PrescriptionRepo:

    async def get_all_prescription(self, session: db_session) -> List[PrescriptionResponse]:
        statement = select(Prescription)
        result = await session.execute(statement)
        Prescription = result.scalars().all()

        return [PrescriptionResponse.model_validate(Prescription) for Prescription in Prescription]
    
    async def get_prescription(self, Prescription_id: str, session: db_session) -> Optional[PrescriptionResponse]:
        statement = select(Prescription).where(Prescription.uid == Prescription_id)
        result = await session.execute(statement)
        Prescription = result.scalars().one_or_none()

        return PrescriptionResponse.model_validate(Prescription) if Prescription else None

    async def create_prescription(self, Prescription_data: PrescriptionCreate, session: db_session) -> PrescriptionResponse:
        new_Prescription = Prescription(**Prescription_data.model_dump())
        session.add(new_Prescription)
        await session.commit()
        await session.refresh(new_Prescription)
        return PrescriptionResponse.model_validate(new_Prescription)
    
    async def update_prescription(self, Prescription_id: str, Prescription: PrescriptionUpdate, session: db_session) -> PrescriptionResponse:
        statement = select(Prescription).where(Prescription.uid == Prescription_id)
        result = await session.execute(statement)
        Prescription_to_update = result.scalars().one_or_none()

        if not Prescription_to_update:
            return None

        for key, value in Prescription.model_dump(exclude_unset=True).items():
            setattr(Prescription_to_update, key, value) 

        await session.commit()
        await session.refresh(Prescription_to_update)
        return PrescriptionResponse.model_validate(Prescription_to_update)
    
    async def delete_prescription(self, Prescription_id: str, session: db_session) -> bool:
        statement = select(Prescription).where(Prescription.uid == Prescription_id)
        result = await session.execute(statement)
        Prescription_to_delete= result.scalars().one_or_none()
        if not Prescription_to_delete:
            return False
        await session.delete(Prescription_to_delete)
        await session.commit()
        return True
    
