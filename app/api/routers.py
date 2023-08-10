from fastapi import APIRouter

from app.api.endpoints.user import router as user_router
from app.api.endpoints.meters import router as meters_router


main_router = APIRouter()
main_router.include_router(user_router, prefix='/user', tags=['users'])
main_router.include_router(meters_router, prefix='/meter', tags=['meters'])
