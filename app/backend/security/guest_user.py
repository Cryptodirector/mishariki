from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert

from app.backend.database import get_async_session
from app.backend.models.v1.users import Users


class GuestUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = Response("Internal server error", status_code=500)

        try:
            session: AsyncSession
            async for session in get_async_session():
                guest_id = request.cookies.get("guest_id")

                if guest_id:
                    try:
                        guest_id = int(guest_id)
                        result = await session.execute(
                            select(Users.id).where(Users.id == guest_id)
                        )
                        user = result.scalar_one_or_none()
                        if user:
                            request.state.guest_id = guest_id
                            response = await call_next(request)
                            return response
                    except (ValueError, TypeError):
                        pass

                # Создаем нового гостя
                result = await session.execute(
                    insert(Users).values(guest=True).returning(Users.id)
                )
                guest_id = result.scalar_one()
                await session.commit()

                request.state.guest_id = guest_id

                response = await call_next(request)
                response.set_cookie("guest_id", str(guest_id), max_age=60 * 60 * 24 * 90)
                return response

        except Exception as e:
            print("Middleware error:", e)
            return response
