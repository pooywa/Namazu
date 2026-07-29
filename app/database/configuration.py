from sqlalchemy import create_engine
from sqlalchemy.orm import Session

#crate engine
engine = create_engine(
    "postgresql+psycopg://earthquakes_user:1234@localhost:5432/earthquakes"
)

#create sessoin 
session = Session(engine)

