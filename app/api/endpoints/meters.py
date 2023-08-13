from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meter_exists
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.meters import meters_crud, data_crud
from app.schemas.meters import MeterCreate, DataDB
from app.models.user import User


router = APIRouter()


@router.get(
    '/stat/{meter_id}',
    response_model=List[DataDB],
    response_model_exclude_none=True,
)
async def get_meter_data(
    meter_id: int,
    start: datetime,
    end: datetime,
    session: AsyncSession = Depends(get_async_session),
):
    """запрос показаний счетчика за период"""
    meter = await check_meter_exists(meter_id, session)
    data = await data_crud.get_data_stat(meter, start, end, session)
    return data


@router.get(
    '/{meter_id}',
    response_model=DataDB,
    response_model_exclude_none=True,
)
async def get_meter_current_data(
    meter_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """запрос текущего состояния счетчика"""
    meter = await check_meter_exists(meter_id, session)
    data = await data_crud.get_data_current(meter, session)
    return data


@router.post(
    '/',
    response_model=MeterCreate,
    response_model_exclude_none=True,
)
async def create_new_meter(
    meter: MeterCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """создание нового счетчика"""
    new_meter = await meters_crud.create(meter, session, user)
    return new_meter


@router.delete(
    '/{meter_id}',
    response_model=MeterCreate,
    dependencies=[Depends(current_user)],
)
async def remove_project(
    meter_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """удаление счетчика"""
    meter = await check_meter_exists(meter_id, session)
    meter = await meters_crud.remove(meter, session)
    return meter
