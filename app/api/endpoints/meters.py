from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_exists,
                                check_invested_amount, check_full_amount,
                                check_closed)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectBase, CharityProjectDB, CharityProjectCreate,
    CharityProjectDelete
)
from app.core.user import current_superuser
from app.services.investing import investing_in_new_project


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    new_project = await investing_in_new_project(new_project, session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDelete,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    await check_invested_amount(project.invested_amount)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectBase,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    await check_closed(project.fully_invested)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount(project.invested_amount, obj_in.full_amount)
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    if project.full_amount == project.invested_amount:
        project = await charity_project_crud.update_fully_invested(
            project, session
        )
    return project
