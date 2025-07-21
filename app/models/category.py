from sqlalchemy import BigInteger, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    yandex_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    parent_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True
    )

    # Отношения для родителя и потомков
    parent: Mapped[Optional["Category"]] = relationship(
        back_populates="children",
        remote_side=[id],
    )
    children: Mapped[List["Category"]] = relationship(
        back_populates="parent",
        cascade="all, delete",
    )
