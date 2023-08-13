import asyncio
from datetime import datetime
import logging
import os
import sys
import time
from typing import Dict

from aiohttp import ClientSession
import requests_async as requests
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from app.core.config import settings  # noqa
from app.models.meters import Data  # noqa


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_session():
    """получение сессии"""
    engine = create_async_engine(settings.database_url)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
    return scoped_session(AsyncSessionLocal)


async def get_meter_data(port: int):
    """запрос данных счетчика"""
    async with ClientSession() as session:
        url = f'https://127.0.0.1:{port}/'
        try:
            async with session.get(url=url) as response:
                data = await response.json()
                data['data_datetime'] = datetime.now()
        except requests.exceptions as error:
            raise ConnectionError(f'ошибка {error} запроса к url {url}')
        return data


async def check_response(data: Dict):
    """проверка ответа"""
    if len(data) != 4:
        raise ValueError('в ответе API недостаточно данных')
    if 'id' not in data:
        raise KeyError('в ответе API отсутствует номер счетчика')
    if 'A' not in data:
        raise KeyError('в ответе API отсутствует текущий ток')
    if 'kW' not in data:
        raise KeyError('в ответе API отсутствует потребление энергии')


async def save_data(
    data: Dict,
    session: AsyncSession = get_session(),
):
    """сохранение данных в базу"""
    db_obj = Data(
        meter_id=data['id'],
        data_datetime=data['data_datetime'],
        ampers=data['A'],
        watts=data['kW']
    )
    session.add(db_obj)
    await session.commit()


async def main():
    """опрос счетчиков"""
    while True:
        try:
            logger.info('старт опроса счатчиков')
            for port in range(settings.start_port, settings.end_port + 1):
                data = await get_meter_data(port)
                await check_response(data)
                await save_data(data)
        except Exception as error:
            logger.error(f'сбой в работе программы: {error}')
        finally:
            time.sleep(settings.time_step_sec)


if __name__ == '__main__':
    asyncio.run(main())
