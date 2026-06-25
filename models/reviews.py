import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.setting import Base, id_type, engine, Rate
from sqlalchemy import ForeignKey, text
from models.users import UsersOrm
from models.drivers import DriverOrm
class ReviewsOrm(Base):
    __tablename__ = "reviews"

    id: Mapped[id_type] = mapped_column(unique=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rate: Mapped[Rate]
    text: Mapped[str]
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.date.today())

Base.metadata.create_all(engine)
