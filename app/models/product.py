from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    price: Mapped[float] = mapped_column(Float, nullable=False)

    stock: Mapped[int] = mapped_column(Integer, nullable=False)