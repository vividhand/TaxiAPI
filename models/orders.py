import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.setting import Base, id_type, OrderStatus
from sqlalchemy import ForeignKey, text
from models.drivers import DriverOrm
from models.users import UsersOrm
class OrdersOrm(Base):
    __tablename__ = "orders"

    id: Mapped[id_type]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    date: Mapped[datetime.datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    status: Mapped[OrderStatus] = mapped_column(default="waiting")

from core.setting import engine, Base
Base.metadata.create_all(engine)