from sqlalchemy import Column, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.db import Base


class Meters(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    create_date = Column(DateTime)

    data = relationship('Data', back_populates='meters')


class Data(Base):
    meter_id = Column(Integer, ForeignKey('meters.id'))
    data_datetime = Column(DateTime)
    ampers = Column('A', Integer, nullable=False)
    watts = Column('kW', Integer, nullable=False)

    meters = relationship('Meters', back_populates='data', cascade='delete')
