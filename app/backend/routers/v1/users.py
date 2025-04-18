from fastapi import APIRouter, Depends, Request, Form, Response

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database import get_async_session
from app.backend.schemas.v1.users import UserFormSchemas
from app.backend.service.v1.users import UsersService, ProdUserService

router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.post('/add_user')
async def add(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    await UsersService.add_users(
        request=request,
        session=session
    )


@router.post('/add_favorites_product/{product_id}')
async def add(
        request: Request,
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    await ProdUserService.add_prod_user(
        request=request,
        product_id=product_id,
        session=session
    )


@router.get('/my_favorites_product')
async def get_prod_user(
        request: Request,
        session: AsyncSession = Depends(get_async_session),

):
    return await ProdUserService.get_prod_user(
        session=session,
        request=request
    )


@router.post('/my_favorites_product/delete/{id}')
async def delete_prod_user(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    return await ProdUserService.delete_prod_in_favorites(
        id=id,
        session=session
    )


@router.post('/user_form')
async def get_user_form(
        body: UserFormSchemas = Form()
):
    return body


@router.get('/count_prod_user')
async def get_count_user_prod(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    return await ProdUserService.get_count_prod_user(
        request=request,
        session=session,

    )

