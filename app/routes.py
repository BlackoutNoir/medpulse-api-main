from fastapi import APIRouter

# import template
# from app.entities.object.routes import object_router
from app.entities.user_settings.routes import user_settings_router
from app.handlers.auth.routes import auth_router
from app.entities.user.routes import user_router
from app.entities.log.routes import log_router
from app.entities.chat.routes import chat_router
from app.entities.page.routes import page_router
from app.entities.department.routes import department_router
from app.entities.role.routes import role_router  
from app.entities.staff.routes import staff_router
from app.entities.doctor.routes import doctor_router


api_router = APIRouter()

## router templaate
# router.include_router(object_router, prefix="/objects", tags=["Objects"])


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(log_router, prefix="/logs", tags=["logs"])
api_router.include_router(chat_router, prefix="/chats", tags=["chats"])
api_router.include_router(page_router, prefix="/pages", tags=["pages"]) 
api_router.include_router(department_router, prefix="/departments", tags=["departments"])
api_router.include_router(role_router,prefix="/roles",tags=["roles"])
api_router.include_router(staff_router,prefix="/staffs",tags=["staffs"])
api_router.include_router(doctor_router,prefix="/doctors",tags=["doctors"])



api_router.include_router(user_settings_router, prefix="/settings", tags=["settings"])

