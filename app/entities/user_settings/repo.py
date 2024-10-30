from typing import List, Optional
from app.db.models import Settings
from app.db.main import db_session
from app.entities.user_settings.schema import SettingsCreate, SettingsUpdate, SettingsResponse
from sqlmodel import select

class UserSettingsRepo:

    async def get_all_settings(self, session: db_session) -> List[SettingsResponse]:
        statement = select(Settings)
        result = await session.execute(statement)
        settings = result.scalars().all()

        return [SettingsResponse.model_validate(setting) for setting in settings]
    
    async def get_setting(self, settings_id: str, session: db_session) -> Optional[SettingsResponse]:
        statement = select(Settings).where(Settings.uid == settings_id)
        result = await session.execute(statement)
        setting = result.scalars().one_or_none()

        return SettingsResponse.model_validate(setting) if setting else None

    async def create_setting(self, setting: SettingsCreate, session: db_session) -> SettingsResponse:
        new_setting = Settings(**setting.model_dump())
        session.add(new_setting)
        await session.commit()
        await session.refresh(new_setting)
        return SettingsResponse.model_validate(new_setting)
    
    async def update_setting(self, settings_id: str, setting: SettingsUpdate, session: db_session) -> SettingsResponse:
        statement = select(Settings).where(Settings.uid == settings_id)
        result = await session.execute(statement)
        setting_to_update = result.scalars().one_or_none()

        if not setting_to_update:
            return None

        for key, value in setting.model_dump(exclude_unset=True).items():
            setattr(setting_to_update, key, value) 

        await session.commit()
        await session.refresh(setting_to_update)
        return SettingsResponse.model_validate(setting_to_update)
    
    async def delete_setting(self, settings_id: str, session: db_session) -> bool:
        statement = select(Settings).where(Settings.uid == settings_id)
        result = await session.execute(statement)
        setting_to_delete= result.scalars().one_or_none()
        if not setting_to_delete:
            return False
        await session.delete(setting_to_delete)
        await session.commit()
        return True
    
