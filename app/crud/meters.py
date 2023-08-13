from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meters import Data, Meters


class CRUDData(CRUDBase):

    async def get_data_stat(
        self,
        meter: Meters,
        start: datetime,
        end: datetime,
        session: AsyncSession
    ) -> Optional[List[Data]]:
        db_objs = await session.execute(select(self.model).where(
            self.model.meter_id == meter.id, and_(
                self.model.data_datetime >= start,
                self.model.data_datetime <= end
            )
        ))
        return db_objs.scalars().all()

    async def get_data_current(
        self,
        meter: Meters,
        session: AsyncSession
    ) -> Optional[Data]:
        db_objs = await session.execute(select(self.model).where(
            self.model.meter_id == meter.id
        ).order_by(self.model.data_datetime.desc()))
        return db_objs.scalars().first()


data_crud = CRUDData(Data)
meters_crud = CRUDBase(Meters)
