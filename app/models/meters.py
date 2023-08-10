from datetime import datetime

from sqlalchemy import (Column, Text, DateTime, ForeignKey, Computed, Integer,
                        CheckConstraint, String, UniqueConstraint, Float)
from sqlalchemy.orm import relationship

from app.core.db import Base


class Meters(Base):
    comment = Column(Text)


class Data(Base):
    meters_id = Column(Integer, ForeignKey('meters.id'))
    data_datetime = Column(DateTime, default=datetime.now)
    amper = Column('A', Integer, nullable=False)
    kilowats = Column('kW', Integer, nullable=False)

    meters = relationship('Meters', back_populates='data')

    __table_args__ = (
        UniqueConstraint('meters_id', 'data_datetime'),
    )
