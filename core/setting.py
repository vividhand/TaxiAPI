from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from sqlalchemy.orm import mapped_column
from typing import Annotated
import enum

id_type = Annotated[int, mapped_column(primary_key=True)]
load_dotenv()
url = f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}"
engine = create_engine(url=url, echo=False)

class Base(DeclarativeBase):
    ...
session = sessionmaker(engine)

class UserStatus(enum.Enum):
    inactive = "inactive"
    waiting = "waiting"
    on_way = "on_way"

class OrderStatus(enum.Enum):
    on_way = "on_way"
    waiting = "waiting"
    completed = "completed"

class DriverStatus(enum.Enum):
    active = "active"
    banned = "banned"

class Rate(enum.Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

