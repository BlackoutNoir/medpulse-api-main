from typing import List, Optional
from app.db.models import Log
from app.db.main import db_session
from app.entities.log.schema import LogResponse, LogCreate, LogUpdate, LogFilter 
from sqlmodel import select, and_


class LogRepo:

    async def get_all_logs(self, session: db_session) -> List[LogResponse]:
        statement = select(Log).order_by(Log.timestamp)
        result = await session.execute(statement)
        logs = result.scalars().all()

        return [LogResponse.model_validate(log) for log in logs]
    
    async def get_log(self, log_id: str, session: db_session) -> Optional[LogResponse]:
        statement = select(Log).where(Log.uid == log_id)
        result = await session.execute(statement)
        log = result.scalars().one_or_none()

        return LogResponse.model_validate(log) if log else None
    
    async def create_log(self, log_data: LogCreate, session: db_session) -> LogResponse:
      
        new_log = Log(**log_data.model_dump())
        session.add(new_log)
        await session.commit()
        await session.refresh(new_log)

        return LogResponse.model_validate(new_log)
    
    async def update_log(self, log_id: str, log: LogUpdate, session: db_session) -> LogResponse:
        statement = select(Log).where(Log.uid == log_id)
        result = await session.execute(statement)
        log_to_update = result.scalars().one_or_none()

        if not log_to_update:
            return None

        for key, value in log.model_dump(exclude_unset=True).items():
            setattr(log_to_update, key, value) 
        
        await session.commit()
        await session.refresh(log_to_update)
        return LogResponse.model_validate(log_to_update)
    
    async def delete_log(self, log_id: str, session: db_session) -> bool:
        statement = select(Log).where(Log.uid == log_id)
        result = await session.execute(statement)
        log_to_delete= result.scalars().one_or_none()
        if not log_to_delete:
            return False
        await session.delete(log_to_delete)
        await session.commit()
        return True 
    

    async def filter_logs(self, filters: LogFilter, session: db_session) -> List[LogResponse]:

        statement = select(Log)
        

        partial_match_fields = [
            "description"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            column = getattr(Log, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        result = await session.execute(statement)
        logs = result.scalars().all()

        return [LogResponse.model_validate(log) for log in logs]