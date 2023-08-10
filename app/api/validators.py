from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_full_amount(
    invested_amount: int,
    full_amount: int,
) -> None:
    if invested_amount > full_amount:
        raise HTTPException(
            status_code=400,
            detail='Сумма проекта не может быть меньше уже инвестированной!',
        )


async def check_invested_amount(
    invested_amount: int,
) -> None:
    if invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_closed(
    fully_invested: bool,
) -> None:
    if fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_range(
    rowCount: int,
) -> None:
    if rowCount > 30:
        raise HTTPException(
            status_code=400,
            detail='Количество строк более 30 - увеличь размер репорта!',
        )
