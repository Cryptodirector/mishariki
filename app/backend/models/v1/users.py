from app.backend.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.backend.models.v1.products import Products


class ProductsUsers(Base):
    __tablename__ = 'products_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_products: Mapped[int] = mapped_column(
        ForeignKey('products.id'),
        nullable=False
    )
    id_users: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )
    product: Mapped['Products'] = relationship(
        back_populates='prod_user'
    )
    user: Mapped['Users'] = relationship(
        back_populates='prod_user'
    )


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    guest: Mapped[bool] = mapped_column(default=True)

    prod_user: Mapped['ProductsUsers'] = relationship(
        back_populates='user'
    )




