from fastapi import APIRouter

# import template
# from app.entities.object.routes import object_router
from app.entities.user_settings.routes import user_settings_router


api_router = APIRouter()

## router templaate
# router.include_router(object_router, prefix="/objects", tags=["Objects"])

api_router.include_router(user_settings_router, prefix="/settings", tags=["settings"])