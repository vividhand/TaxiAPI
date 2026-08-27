from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column
from core.setting import Base, id_type, engine
from sqlalchemy import ForeignKey
from models.users import UsersOrm
from models.drivers import DriverOrm
from models.orders import OrdersOrm
class ReviewsOrm(Base):
    __tablename__ = "reviews"

    id: Mapped[id_type] = mapped_column(unique=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rate: Mapped[int]
    text: Mapped[str]
    date: Mapped[datetime] = mapped_column(default=datetime.now(UTC))