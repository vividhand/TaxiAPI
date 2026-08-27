from datetime import datetime, UTC, timedelta
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from core.setting import engine
from models import UsersOrm, EmailVerificationOrm

class EmailVerifyRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_code(self, email: str, code: int, token: str) -> bool:
        with self.session as sess:
            user_id_request = select(UsersOrm.id).where(UsersOrm.email == email)
            response = sess.execute(user_id_request).scalar_one_or_none()
            if response is None:
                return False
            request = EmailVerificationOrm(user_id= response, code= code, expires_at= (datetime.now(UTC) + timedelta(minutes=5)), token= token)
            sess.add(request)
            sess.commit()
            return True

    def get_code_data_by_token(self, token) -> EmailVerificationOrm:
        with self.session as sess:
            request = select(EmailVerificationOrm).where(EmailVerificationOrm.token == token)
            response = sess.execute(request).scalars().first()
            return response

    def select_expired_time(self, token):
        with self.session as sess:
            request = select(EmailVerificationOrm.expires_at).where(EmailVerificationOrm.token == token)
            response = sess.execute(request).scalar_one()
            return response

    def update_status(self, token: str) -> None:
        with self.session as sess:
            user_id_request = select(UsersOrm.id).join(EmailVerificationOrm, EmailVerificationOrm.user_id == UsersOrm.id).where(EmailVerificationOrm.token == token)
            response = sess.execute(user_id_request).first()[0]
            request_update_user = update(UsersOrm).where(UsersOrm.id == response).values(is_verified=True)
            request_update_email = update(EmailVerificationOrm).where(EmailVerificationOrm.user_id == response).values(it_expired=True)
            sess.execute(request_update_user)
            sess.execute(request_update_email)
            sess.commit()

    def deactivate_old_code(self, user_id: int) -> None:
        with self.session as sess:
            request_select = select(EmailVerificationOrm.token).join(UsersOrm, EmailVerificationOrm.user_id == UsersOrm.id).where(UsersOrm.id == user_id)
            token = sess.execute(request_select)
            request_delete = delete(EmailVerifyRepositories).where(EmailVerificationOrm.token == token)
            sess.execute(request_delete)
            sess.commit()

