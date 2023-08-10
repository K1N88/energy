from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'well statistic'
    app_description: str = 'данные по скважинам пробуренным в компании'
    app_author: str = 'kn'
    database_url: str = 'sqlite+aiosqlite:///./workapi.db'
    admin_database_url: str = 'sqlite:///./workapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    first_superuser_name: Optional[str] = None
    first_superuser_last_name: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
