from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database import get_async_session
from app.backend.service.v1.popular_products import PopularProductsService

router = APIRouter(
    prefix='/popular_products',
    tags=['Категория']
)


@router.post('/add')
async def add_products(
        name: str,
        descriptions: str,
        price: int,
        old_price: int,
        url_photo: str,
        session: AsyncSession = Depends(get_async_session)

):
    return await PopularProductsService.insert_popular_products(
        name=name,
        descriptions=descriptions,
        price=price,
        old_price=old_price,
        url_photo=url_photo,
        session=session
    )


@router.post('/{id}/update')
async def add_products(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        name: str | None = Form(None),
        descriptions: str | None = Form(None),
        price: int | None = Form(None),
        old_price: int | None = Form(None),
        url_photo: str | None = Form(None),


):
    return await PopularProductsService.path_popular_product(
        name=name,
        descriptions=descriptions,
        price=price,
        old_price=old_price,
        url_photo=url_photo,
        session=session,
        id=id
    )


@router.get('/all')
async def get_all_popular_products(
        session: AsyncSession = Depends(get_async_session)
):
    return await PopularProductsService.get_popular_products(
        session=session
    )