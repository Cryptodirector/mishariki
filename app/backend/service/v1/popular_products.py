from fastapi import Form
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.models.v1.popular_products import PopularProducts


class PopularProductsService:

    @staticmethod
    async def path_popular_product(
            id: int,
            session: AsyncSession,
            name: str | None = Form(None),
            descriptions: str | None = Form(None),
            price: int | None = Form(None),
            old_price: int | None = Form(None),
            url_photo: str | None = Form(None),

    ):
        await session.execute(
            update(PopularProducts).values(
                name=name,
                descriptions=descriptions,
                price=price,
                old_price=old_price,
                url_photo=url_photo
            ).where(PopularProducts.id == id)
        )

    @staticmethod
    async def get_popular_products(
            session: AsyncSession
    ):
        result = await session.execute(
            select(PopularProducts)
        )
        return result.scalars().all()

    @staticmethod
    async def get_popular_product_id(
            id: int,
            session: AsyncSession
    ):
        result = await session.execute(
            select(PopularProducts).where(PopularProducts.id == id)
        )
        return result.scalars().all()

    @staticmethod
    async def insert_popular_products(
            name: str,
            descriptions: str,
            price: int,
            old_price: int,
            url_photo: int,
            session: AsyncSession
    ):

        await session.execute(
            insert(PopularProducts).values(
                name=name,
                descriptions=descriptions,
                price=price,
                old_price=old_price,
                url_photo=url_photo
            )
        )
