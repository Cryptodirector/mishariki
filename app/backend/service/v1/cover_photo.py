from fastapi import Form
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.models.v1.photo_cover import PhotoCover


class CoverPhotoService:

    @staticmethod
    async def add_cover_photo(
            url_photo: str,
            session: AsyncSession
    ):
        await session.execute(
            insert(PhotoCover).values(url_photo=url_photo)
        )

        await session.commit()

    @staticmethod
    async def update_photo_cover(
            id: int,
            url: str,
            session: AsyncSession
    ):
        await session.execute(
            update(PhotoCover).values(
                url=url
            ).where(PhotoCover.id == id)
        )

        await session.commit()

    @staticmethod
    async def get_cover_photo(
            session: AsyncSession
    ):
        result = await session.execute(
            select(PhotoCover)
        )
        return result.scalars().all()

    @staticmethod
    async def get_cover_photo_id(
            id: int,
            session: AsyncSession
    ):
        result = await session.execute(
            select(PhotoCover).where(PhotoCover.id == id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_cover_1(
            session: AsyncSession
    ):
        result = await session.execute(
            select(PhotoCover).where(PhotoCover.id == 1)
        )
        return result.scalars().all()

    @staticmethod
    async def get_cover_2(
            session: AsyncSession
    ):
        result = await session.execute(
            select(PhotoCover).where(PhotoCover.id == 2)
        )
        return result.scalars().all()

    @staticmethod
    async def get_cover_3(
            session: AsyncSession
    ):
        result = await session.execute(
            select(PhotoCover).where(PhotoCover.id == 3)
        )
        return result.scalars().all()