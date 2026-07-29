from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os 
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")
#crate engine
engine = create_engine(
    f"postgresql+psycopg://{db_user}:{db_password}@localhost:5432/earthquakes_db"
)

#create sessoin 
session = Session(engine)

