from sqlalchemy import ForeignKey, DateTime
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.setting import Base, id_type, engine
from models.users import UsersOrm
class RefreshTokensOrm(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[id_type]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column(default=False)

