from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meters import meters_crud
from app.models.meters import Meters


async def check_meter_exists(
    meter_id: int,
    session: AsyncSession,
) -> Meters:
    meter = await meters_crud.get(meter_id, session)
    if meter is None:
        raise HTTPException(
            status_code=404,
            detail='счетчик не найден!'
        )
    return meter
