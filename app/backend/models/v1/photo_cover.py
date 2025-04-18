from app.backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class PhotoCover(Base):
    __tablename__ = 'user_photo_cover'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)


