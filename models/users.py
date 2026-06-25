import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.setting import Base, id_type, engine
from sqlalchemy import String, text

class UsersOrm(Base):
    __tablename__ = "users"
    metadata = Base.metadata

    id: Mapped[id_type]
    fullname: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[bytes] = mapped_column(String(255))
    registration_date: Mapped[datetime.datetime] = mapped_column(server_default=text("timezone('utc', now())"))
    is_admin: Mapped[bool] = mapped_column(server_default=text("False"))
    is_verified: Mapped[bool] = mapped_column(server_default=text("False"))

Base.metadata.create_all(engine)