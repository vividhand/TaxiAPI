from core.setting import engine
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select
from models import UsersOrm, EmailVerificationOrm
from typing import Optional

class UserRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_user(self, full_name: str, email: str, password: str) -> bool:
            with self.session as sess:
                new_user = UsersOrm(fullname=full_name, email=email, password=password)
                sess.add(new_user)
                sess.commit()
                return True

    def select_user_by_verification_token(self, token: str) -> Optional[UsersOrm]:
        with self.session as sess:
            query = select(UsersOrm).select_from(UsersOrm).join(EmailVerificationOrm, EmailVerificationOrm.user_id == UsersOrm.id).where(EmailVerificationOrm.token == token)
            user = sess.execute(query).scalars().first()
            return user

    def select_user_by_email(self, email: str) -> Optional[UsersOrm]:
        with self.session as sess:
            query = select(UsersOrm).where(UsersOrm.email == email)
            user = sess.execute(query).scalars().first()
            return user
    def select_user_by_id(self, user_id: int) -> Optional[UsersOrm]:
        with self.session as sess:
            query = select(UsersOrm).where(UsersOrm.id == user_id)
            user = sess.execute(query).scalars().first()
            return user











