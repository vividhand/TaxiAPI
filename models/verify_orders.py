from sqlalchemy import ForeignKey, DateTime
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.setting import Base, id_type
from models.drivers import DriverOrm
from models.orders import OrdersOrm
class OrdersVerificationOrm(Base):
    __tablename__ = "order_verification"

    order_id: Mapped[id_type] = mapped_column(ForeignKey("orders.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    code: Mapped[int]
    token: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    it_expired: Mapped[bool] = mapped_column(default=False)

from core.setting import engine, Base
Base.metadata.create_all(engine)