from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.setting import Base, id_type
from sqlalchemy import ForeignKey


class CarsOrm(Base):
    __tablename__ = "cars"
    metadata = Base.metadata

    id: Mapped[id_type]
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    plate_number: Mapped[str]
    brand: Mapped[str]
    look: Mapped[str]
