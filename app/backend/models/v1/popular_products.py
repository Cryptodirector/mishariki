from app.backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class PopularProducts(Base):
    __tablename__ = 'popular_products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    descriptions: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=True)
    old_price: Mapped[int] = mapped_column(nullable=True)
    url_photo: Mapped[str] = mapped_column(nullable=True)
