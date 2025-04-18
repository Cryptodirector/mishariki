from fastapi import Form
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.models.v1.popular_products import PopularProducts
from app.backend.models.v1.products import Products


async def get_product_for_order(
        id: int,
        session: AsyncSession
):
    result = await session.execute(
        select(Products).where(Products.id == id)
    )

    return result.mappings().all()