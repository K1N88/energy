from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field, Extra


class MeterCreate(BaseModel):
    create_date: Optional[datetime] = datetime.now()
    comment: Optional[str] = None

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DataDB(BaseModel):
    meter_id: int
    data_datetime: datetime
    ampers: PositiveInt = Field(None, exclusiveMinimum=0)
    watts: PositiveInt = Field(None, exclusiveMinimum=0)

    class Config:
        extra = Extra.forbid
        orm_mode = True
