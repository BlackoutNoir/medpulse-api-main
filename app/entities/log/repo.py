from typing import List, Optional
from app.db.models import Log
from app.db.main import db_session
from app.entities.log.schema import LogCreate, LogUpdate, LogResponse
from sqlmodel import select

class LogRepo:

    async def get_all_Log(self, session: db_session) -> List[LogResponse]:
        statement = select(Log)
        result = await session.execute(statement)
        Log = result.scalars().all()

        return [LogResponse.model_validate(setting) for setting in Log]
    
    async def get_setting(self, Log_id: str, session: db_session) -> Optional[LogResponse]:
        statement = select(Log).where(Log.uid == Log_id)
        result = await session.execute(statement)
        setting = result.scalars().one_or_none()

        return LogResponse.model_validate(setting) if setting else None

    async def create_setting(self, setting_data: LogCreate, session: db_session) -> LogResponse:
        new_setting = Log(**setting_data.model_dump())
        session.add(new_setting)
        await session.commit()
        await session.refresh(new_setting)
        return LogResponse.model_validate(new_setting)
    
    async def update_setting(self, Log_id: str, setting: LogUpdate, session: db_session) -> LogResponse:
        statement = select(Log).where(Log.uid == Log_id)
        result = await session.execute(statement)
        setting_to_update = result.scalars().one_or_none()

        if not setting_to_update:
            return None

        for key, value in setting.model_dump(exclude_unset=True).items():
            setattr(setting_to_update, key, value) 

        await session.commit()
        await session.refresh(setting_to_update)
        return LogResponse.model_validate(setting_to_update)
    
    async def delete_setting(self, Log_id: str, session: db_session) -> bool:
        statement = select(Log).where(Log.uid == Log_id)
        result = await session.execute(statement)
        setting_to_delete= result.scalars().one_or_none()
        if not setting_to_delete:
            return False
        await session.delete(setting_to_delete)
        await session.commit()
        return True
    
