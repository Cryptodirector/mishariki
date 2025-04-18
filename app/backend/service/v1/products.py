from fastapi import Form
from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.models.v1.products import Products, Categories
from app.backend.schemas.v1.products import ProductsSchemas, CategoriesSchemas


class ProductsService:

    @staticmethod
    async def add_products(
            session: AsyncSession,
            body: ProductsSchemas
    ) -> ProductsSchemas:
        await session.execute(
            insert(Products).values(body.model_dump())
        )
        await session.commit()
        return body

    @staticmethod
    async def update_products(
            session: AsyncSession,
            id: int,
            name: str | None = Form(None),
            descriptions: str | None = Form(None),
            price: int | None = Form(None),
            old_price: int | None = Form(None),
            url_photo: str | None = Form(None),
    ) -> ProductsSchemas:
        await session.execute(
            update(Products).values(
                name=name,
                descriptions=descriptions,
                price=price,
                old_price=old_price,
                url_photo=url_photo
            ).where(Products.id == id)
        )
        await session.commit()

    @staticmethod
    async def get_products(
            session: AsyncSession
    ):

        result = await session.execute(
            select(Products)
        )
        return result.scalars().all()

    @staticmethod
    async def get_product(
            id: int,
            session: AsyncSession
    ):

        result = await session.execute(
            select(Products).where(Products.id == id)
        )
        return result.scalars().all()

    @staticmethod
    async def delete_product(
            id: int,
            session: AsyncSession
    ):
        await session.execute(
            delete(Products).where(Products.id == id)
        )
        await session.commit()


class CategoriesService:

    @staticmethod
    async def add_categories(
            body: CategoriesSchemas,
            session: AsyncSession
    ) -> CategoriesSchemas:

        await session.execute(
            insert(Categories).values(body.model_dump())
        )

        await session.commit()

        return body

    @staticmethod
    async def get_categories(
            session: AsyncSession
    ):
        result = await session.execute(
            select(Categories)
        )
        return result.scalars().all()

    @staticmethod
    async def get_category(
            id: int,
            session: AsyncSession
    ):

        result = await session.execute(
            select(Categories).where(Categories.id == id)
        )

        return result.scalars().all()

    @staticmethod
    async def delete_cat(
            id: int,
            session: AsyncSession
    ):

        await session.execute(
            delete(Categories).where(Categories.id == id)
        )

        await session.commit()

    @staticmethod
    async def get_all_product_in_category(
            id: int,
            session: AsyncSession
    ):

        result = await session.execute(
            select(
                Products.id,
                Products.name,
                Products.price,
                Products.descriptions,
                Products.categories_id,
                Categories.name.label('category')
            ).join(Categories).where(
                Categories.id == Products.categories_id,
                Categories.id == id
            )
        )
        return result.mappings().all()

    @staticmethod
    async def update_category(
            id: int,
            name: str,
            session: AsyncSession
    ):

        await session.execute(
            update(Categories).values(name=name).where(Categories.id == id)
        )

        await session.commit()