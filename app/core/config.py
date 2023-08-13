from typing import Optional

from pydantic import EmailStr, BaseSettings


class Settings(BaseSettings):
    app_title: str = 'energy meters data'
    app_description: str = 'сбор показаний счетчиков электроэнергии'
    database_url: str = 'sqlite+aiosqlite:///./energyapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    first_superuser_name: Optional[str] = None
    first_superuser_last_name: Optional[str] = None

    time_step_sec: int = 60  # периодичность опроса счетчиков
    start_port: int = 9000  # диапазон адресов/портов начало
    end_port: int = 65000  # диапазон адресов/портов конец

    class Config:
        env_file = '.env'


settings = Settings()
