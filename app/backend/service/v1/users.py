from sqlalchemy import insert, select, func, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Form, Response

from app.backend.models.v1.products import Products
from app.backend.models.v1.users import Users, ProductsUsers
from app.backend.schemas.v1.users import UserFormSchemas


class UsersService:

    @staticmethod
    async def add_users(
            request: Request,
            response: Response,
            session: AsyncSession
    ) -> int:
        guest_id = getattr(request.state, "guest_id", None)

        if guest_id:
            try:
                guest_id = int(guest_id)
                result = await session.execute(select(Users.id).where(Users.id == guest_id))
                user = result.scalar_one_or_none()
                if user:
                    return guest_id
            except (ValueError, TypeError):
                pass

        # создаём нового пользователя
        result = await session.execute(
            insert(Users).values(guest=True).returning(Users.id)
        )
        guest_id = result.scalar_one()
        await session.commit()
        response.set_cookie("guest_id", str(guest_id), max_age=60 * 60 * 24 * 90)
        return response


class ProdUserService:

    @staticmethod
    async def add_prod_user(
            request: Request,
            product_id: int,
            session: AsyncSession,
    ):
        guest_id = getattr(request.state, "guest_id", None)
        user = await session.execute(
            select(Users.id).where(Users.id == int(guest_id))
        )

        await session.execute(
            insert(ProductsUsers).values(
                id_users=user.scalar(),
                id_products=product_id
            )
        )
        await session.commit()

    @staticmethod
    async def get_prod_user(
            session: AsyncSession,
            request: Request
    ):
        guest_id = getattr(request.state, "guest_id", None)
        user = await session.execute(
            select(Users.id).where(Users.id == int(guest_id))
        )
        result = await session.execute(
            select(
                Products,
                ProductsUsers.id.label('lala')
            ).join(ProductsUsers).where(
                user.scalar() == ProductsUsers.id_users
            )
        )
        return result.all()

    @staticmethod
    async def delete_prod_in_favorites(
            id: int,
            session: AsyncSession
    ):
        await session.execute(
            delete(ProductsUsers).where(
                or_(
                    ProductsUsers.id == id,
                    ProductsUsers.id_products == id
                )

            )
        )
        await session.commit()

    @staticmethod
    async def get_count_prod_user(
            request: Request,
            session: AsyncSession
    ):
        guest_id = getattr(request.state, "guest_id", None)

        result = await session.execute(
            select(func.count()).select_from(ProductsUsers).where(
                ProductsUsers.id_users == int(guest_id)
            )
        )

        return {'count': result.scalar()}


class UserForm:

    @staticmethod
    async def user_form(
            body: UserFormSchemas = Form()
    ):
        print(body)
