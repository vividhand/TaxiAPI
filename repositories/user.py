from core.setting import engine
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select
from models import UsersOrm, EmailVerificationOrm, OrdersOrm, DriverOrm
from typing import Optional
class UserRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_user(self, full_name: str, email: str, password: str) -> tuple[bool, str]:
            with self.session as sess:
                new_user = UsersOrm(fullname=full_name, email=email, password=password)
                sess.add(new_user)
                sess.commit()
                return True, "User has been added"

    def select_user_by_verification_token(self, token: str) -> tuple[bool, Optional[UsersOrm, None]]:
        with self.session as sess:
            e = aliased(EmailVerificationOrm)
            query = select(UsersOrm).select_from(UsersOrm).join(e, e.user_id == UsersOrm.id).where(e.token == token)
            user = sess.execute(query).scalars().first()
            if user:
                return True, user
            else:
                return False, None

    def select_user_by_email(self, email: str) -> tuple[bool, Optional[UsersOrm, None]]:
        with self.session as sess:
            query = select(UsersOrm).where(UsersOrm.email == email)
            user = sess.execute(query).scalars().first()
            if user:
                return True, user
            else:
                return False, None

    def select_user_by_id(self, user_id: int) -> tuple[bool, Optional[UsersOrm, None]]:
        with self.session as sess:
            query = select(UsersOrm).where(UsersOrm.id == user_id)
            user = sess.execute(query).scalars().first()
            if user:
                return True, user
            else:
                return False, None









