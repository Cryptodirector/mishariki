from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database import get_async_session
from app.backend.schemas.v1.products import ProductsSchemas, CategoriesSchemas
from app.backend.service.v1.products import ProductsService, CategoriesService

router = APIRouter(
    prefix='/categories',
    tags=['Категория']
)


@router.post('/add')
async def add_cat(
        body: CategoriesSchemas,
        session: AsyncSession = Depends(get_async_session),
):
    return await CategoriesService.add_categories(
        body=body,
        session=session
    )


@router.get('/all')
async def get_all_cat(
        session: AsyncSession = Depends(get_async_session),
):
    return await CategoriesService.get_categories(
        session=session
    )


@router.get('/{id}')
async def get_category_id(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    return await CategoriesService.get_category(
        id=id,
        session=session
    )


@router.post('/{id}/delete')
async def del_cat(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):

    return await CategoriesService.delete_cat(
        id=id,
        session=session
    )


@router.get('/{id}/products')
async def get_prod_in_cat(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):

    return await CategoriesService.get_all_product_in_category(
        id=id,
        session=session
    )

