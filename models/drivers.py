import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.setting import Base, id_type, DriverStatus
from sqlalchemy import ForeignKey, text

class DriverOrm(Base):
    __tablename__ = "drivers"
    metadata = Base.metadata

    id: Mapped[id_type] = mapped_column(ForeignKey("users.id"))
    registration_date: Mapped[datetime.datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    status: Mapped[DriverStatus] = mapped_column(default=DriverStatus.active)