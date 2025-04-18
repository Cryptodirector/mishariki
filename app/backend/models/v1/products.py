from app.backend.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey


class Products(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    descriptions: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=True)
    old_price: Mapped[int] = mapped_column(nullable=True)
    url_photo: Mapped[str] = mapped_column(nullable=True)

    categories_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=True
    )
    categories: Mapped['Categories'] = relationship(back_populates='product')
    prod_user: Mapped['ProductsUsers'] = relationship(
        back_populates='product'
    )


class Categories(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    product: Mapped['Products'] = relationship(
        back_populates='categories'
    )