from typing import List, Optional
from app.db.models import Staff, Schedule
from app.db.main import db_session
from app.entities.staff.schema import StaffCreate, StaffUpdate, StaffResponse, StaffFilter
from sqlmodel import select, and_


class StaffRepo:

    async def get_all_staffs(self, session: db_session) -> List[StaffResponse]:
        statement = select(Staff)
        result = await session.execute(statement)
        staffs = result.scalars().all()

        return [StaffResponse.model_validate(staff) for staff in staffs]
    
    async def get_staff(self, staff_id: str, session: db_session) -> Optional[StaffResponse]:
        statement = select(Staff).where(Staff.uid == staff_id)
        result = await session.execute(statement)
        staff = result.scalars().one_or_none()

        return StaffResponse.model_validate(staff) if staff else None
    
    async def create_staff(self, staff_data: StaffCreate, session: db_session) -> StaffResponse:
        
        new_staff = Staff(**staff_data.model_dump())

        if staff_data.schedules:
            new_staff.schedules = [Schedule(**schedule_data.model_dump()) for schedule_data in staff_data.schedules]
        session.add(new_staff)
        await session.commit()
        await session.refresh(new_staff)

        return StaffResponse.model_validate(new_staff)
    
    async def update_staff(self, staff_id: str, staff: StaffUpdate, session: db_session) -> StaffResponse:
        statement = select(Staff).where(Staff.uid == staff_id)
        result = await session.execute(statement)
        staff_to_update = result.scalars().one_or_none()

        if not staff_to_update:
            return None

        for key, value in staff.model_dump(exclude_unset=True).items():
            if key == "schedule":
                staff_to_update.schedules = [
                    Schedule(**schedule) if isinstance(schedule, dict) else schedule
                    for schedule in value
                ]
            else:
                setattr(staff_to_update, key, value)
        

        await session.commit()
        await session.refresh(staff_to_update)
        return StaffResponse.model_validate(staff_to_update)
    
    async def delete_staff(self, staff_id: str, session: db_session) -> bool:
        statement = select(Staff).where(Staff.uid == staff_id)
        result = await session.execute(statement)
        staff_to_delete= result.scalars().one_or_none()
        if not staff_to_delete:
            return False
        await session.delete(staff_to_delete)
        await session.commit()
        return True 
    

    async def filter_staffs(self, filters: StaffFilter, session: db_session) -> List[StaffResponse]:

        statement = select(Staff)
        

        partial_match_fields = [
            "uuid","name","description"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(Staff, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(Staff, filters.order_by):
            order_column = getattr(Staff, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        staffs = result.scalars().all()

        return [StaffResponse.model_validate(staff) for staff in staffs]