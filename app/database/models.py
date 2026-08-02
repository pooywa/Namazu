from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String, Column


class Base(DeclarativeBase):
    pass

#create table
class Earthquake(Base):
    __tablename__ = "earthquakes"

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[str] = mapped_column(nullable=True)
    latitude:Mapped[str] = mapped_column(nullable=True)
    longitude:Mapped[str] = mapped_column(nullable=True)
    depth: Mapped[str] = mapped_column(String, nullable=True)
    magnitude: Mapped[str] = mapped_column(String, nullable=True)
    place:Mapped[str] = mapped_column(nullable=True)
    source:Mapped[str] = mapped_column(nullable=True)
    month: Mapped[int] = mapped_column(Integer, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    notes:Mapped[str] = mapped_column(String,nullable=True)
