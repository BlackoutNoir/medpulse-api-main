from typing import List, Optional
from app.db.models import Bill
from app.db.main import db_session
from app.entities.bill.schema import BillCreate, BillUpdate, BillResponse
from sqlmodel import select

class BillRepo:

    async def get_all_bill(self, session: db_session) -> List[BillResponse]:
        statement = select(Bill)
        result = await session.execute(statement)
        Bill = result.scalars().all()

        return [BillResponse.model_validate(Bill) for Bill in Bill]
    
    async def get_bill(self, Bill_id: str, session: db_session) -> Optional[BillResponse]:
        statement = select(Bill).where(Bill.uid == Bill_id)
        result = await session.execute(statement)
        Bill = result.scalars().one_or_none()

        return BillResponse.model_validate(Bill) if Bill else None

    async def create_bill(self, Bill_data: BillCreate, session: db_session) -> BillResponse:
        new_Bill = Bill(**Bill_data.model_dump())
        session.add(new_Bill)
        await session.commit()
        await session.refresh(new_Bill)
        return BillResponse.model_validate(new_Bill)
    
    async def update_bill(self, Bill_id: str, Bill: BillUpdate, session: db_session) -> BillResponse:
        statement = select(Bill).where(Bill.uid == Bill_id)
        result = await session.execute(statement)
        Bill_to_update = result.scalars().one_or_none()

        if not Bill_to_update:
            return None

        for key, value in Bill.model_dump(exclude_unset=True).items():
            setattr(Bill_to_update, key, value) 

        await session.commit()
        await session.refresh(Bill_to_update)
        return BillResponse.model_validate(Bill_to_update)
    
    async def delete_bill(self, Bill_id: str, session: db_session) -> bool:
        statement = select(Bill).where(Bill.uid == Bill_id)
        result = await session.execute(statement)
        Bill_to_delete= result.scalars().one_or_none()
        if not Bill_to_delete:
            return False
        await session.delete(Bill_to_delete)
        await session.commit()
        return True
    
