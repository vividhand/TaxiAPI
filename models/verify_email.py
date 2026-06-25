from sqlalchemy import ForeignKey, DateTime
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.setting import Base, id_type
from models.users import UsersOrm
class EmailVerificationOrm(Base):
    __tablename__ = "email_verifications"

    id: Mapped[id_type]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    code: Mapped[int]
    token: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    it_expired: Mapped[bool] = mapped_column(default=False)

