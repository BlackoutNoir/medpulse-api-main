from app.db.main import async_session
from app.db.models import Permission, User, Settings
from app.db.enums import user_type, entity_type, auth_type
from app.handlers.auth.utils import generate_passwd_hash
import asyncio

#To run: python -m app.db.initialize_db

async def initialize_db():
    async with async_session() as session:
            async with session.begin():

                for entity in entity_type:
                    view_permission = Permission(
                        description=f"view {entity.value}",
                    )
                    session.add(view_permission)

                    edit_permission = Permission(
                        description=f"edit {entity.value}",
                    )
                    session.add(edit_permission)

    
                


                admin_user = User(
                    username="admin",
                    email="admin@medpulse.com",
                    firstname="Admin",
                    lastname="User",
                    password_hash=generate_passwd_hash("admin1234"),
                    user_type=user_type.admin,

                )

                session.add(admin_user)
                await session.flush()  
                await session.refresh(admin_user) 

                setting = Settings(
                    user_uid=admin_user.uid,
                    font_size=14,
                    screen_reader=False,
                    on_screen_keyboard=False,
                    email_notifications=True,
                    sms_notifications=False,
                    email_reminders=False,
                    sms_reminders=False,
                    auth_type=auth_type.none
                    )
                session.add(setting)

                
                await session.commit()



                print("Admin user and permissions initialized successfully.")

if __name__ == "__main__":
    asyncio.run(initialize_db())