from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):

    async def get_my_donations(
        self,
        user: User,
        session: AsyncSession
    ) -> Optional[List[Donation]]:
        db_objs = await session.execute(select(self.model).where(
            self.model.user_id == user.id
        ))
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
