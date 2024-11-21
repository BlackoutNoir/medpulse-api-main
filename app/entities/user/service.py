
from app.db.models import Settings
from app.db.main import db_session
from app.entities.user.schema import UserCreate, SettingsCreate, SettingsUpdate
from app.handlers.auth.utils import generate_passwd_hash
import uuid

class UserService:
    async def create_user_settings(self, user_uid: uuid.UUID, session: db_session) -> None:

        settings_data = SettingsCreate(user_uid=user_uid)
        new_settings = Settings(**settings_data.model_dump())
        session.add(new_settings)
        await session.commit()
        await session.refresh(new_settings)

    def hash_passwd(self, password: str) -> str:
        return generate_passwd_hash(password)
    
    