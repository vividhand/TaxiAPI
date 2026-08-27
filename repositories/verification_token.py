from core.setting import engine
from sqlalchemy.orm import Session
from sqlalchemy import select, update,delete
from datetime import datetime
from models.refresh_tokens import RefreshTokensOrm

class RefreshTokensRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_refresh_token(self, user_id: int, token_hash: str, expires_at: datetime, jti: str) -> None:
        with self.session as sess:
            new_refresh_token = RefreshTokensOrm(user_id = user_id, token_hash=token_hash, expires_at=expires_at, jti=jti)
            sess.add(new_refresh_token)
            sess.commit()

    def get_token_data_by_user_id(self, user_id: int) -> RefreshTokensOrm:
        with self.session as sess:
            request = select(RefreshTokensOrm).select_from(RefreshTokensOrm).where((RefreshTokensOrm.user_id == user_id) & (RefreshTokensOrm.is_revoked.is_(False)))
            response = sess.execute(request).scalars().first()
            return response


    def delete_token_data_by_user_id(self, user_id: int):
        with self.session as sess:
            request = delete(RefreshTokensOrm).where(RefreshTokensOrm.user_id == user_id)
            sess.execute(request)
            sess.commit()


    def get_token_data_by_jti(self, jti: str) -> RefreshTokensOrm:
        with self.session as sess:
            request = select(RefreshTokensOrm).where((RefreshTokensOrm.jti == jti) & (RefreshTokensOrm.is_revoked.is_(False)))
            response = sess.execute(request).scalars().first()
            return response


    def delete_token_data_by_jti(self, jti: str):
        with self.session as sess:
            request = delete(RefreshTokensOrm).where(RefreshTokensOrm.jti == jti)
            sess.execute(request)
            sess.commit()

    def revoke_token(self, jti: str):
        with self.session as sess:
            request = update(RefreshTokensOrm).where(RefreshTokensOrm.jti == jti).values(is_revoked = True)
            sess.execute(request)
            sess.commit()