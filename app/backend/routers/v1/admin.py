from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database import get_async_session
from app.backend.service.v1.cover_photo import CoverPhotoService

router = APIRouter(
    prefix='/admin',
    tags=['Админ Панель']
)
