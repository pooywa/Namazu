from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass

#create table
class Earthquake(Base):
    __tablename__ = "earthquakes"

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[str] = mapped_column(nullable=True)
    latitude:Mapped[str] = mapped_column(nullable=True)
    longitude:Mapped[str] = mapped_column(nullable=True)
    depth:Mapped[str] = mapped_column(nullable=True)
    magnitude:Mapped[str] = mapped_column(nullable=True)
    place:Mapped[str] = mapped_column(nullable=True)
    source:Mapped[str] = mapped_column(nullable=True)