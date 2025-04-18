from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.backend.database import get_async_session
from app.backend.service.v1.cover_photo import CoverPhotoService

router = APIRouter(
    prefix='/cover_photo',
    tags=['Обложка']
)


@router.post('/add')
async def add_photo(
        url_photo: str = Form(),
        session: AsyncSession = Depends(get_async_session)
):
    return await CoverPhotoService.add_cover_photo(
        url_photo=url_photo,
        session=session
    )


@router.post('/update/{id}')
async def update_photo(
        id: int,
        url: str = Form(),
        session: AsyncSession = Depends(get_async_session)
):
    await CoverPhotoService.update_photo_cover(
        id=id,
        url=url,
        session=session
    )
    return RedirectResponse(url='/admin', status_code=303)


@router.get('/all')
async def get_photos(
        session: AsyncSession = Depends(get_async_session)
):
    return await CoverPhotoService.get_cover_photo(
        session=session
    )


@router.get('/{id}')
async def get_photo(
        id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await CoverPhotoService.get_cover_photo_id(
        id=id,
        session=session
    )