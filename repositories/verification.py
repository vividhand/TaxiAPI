from core.setting import engine
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, update,delete, Text
from models.users import UsersOrm
from models.verify_email import EmailVerificationOrm
from datetime import datetime, timedelta, UTC
from core.setting import OrderStatus

class EmailVerifyRepositories:
    def __init__(self):
        self.session = Session(engine)
    def add_code(self, email: str, code: int, token: str):
        try:
            with self.session as sess:
                u = aliased(UsersOrm)
                user_id_request = select(u.id).where(u.email == email)
                user_id = sess.execute(user_id_request).scalar_one_or_none()
                if not user_id:
                    return [False, "Email not found"]
                verify = EmailVerificationOrm(user_id = user_id, code=code, expires_at=(datetime.now(UTC) + timedelta(minutes=5)), token=token)
                sess.add(verify)
                sess.commit()
                return True
        except Exception as e:
            sess.rollback()
            return [False, e]

    def get_code_data_by_token(self, token):
        with self.session as sess:
            request = select(EmailVerificationOrm).where(EmailVerificationOrm.token == token)
            code = sess.execute(request).scalars().first()
            return code

    def select_expired_time(self, token):
        try:
            with self.session as sess:
                e = aliased(EmailVerificationOrm)
                expired_time = sess.execute(select(e.expires_at).select_from(e).where(e.token == token)).scalar_one()
                return expired_time
        except Exception as e:
            return [False, e]
    def update_status(self, token: str) -> None:
        with self.session as sess:
            e = aliased(EmailVerificationOrm)
            u = aliased(UsersOrm)
            user_id_request = select(u.id).select_from(u).join(e, e.user_id == u.id).where(e.token == token)
            user_id = sess.execute(user_id_request).first()[0]
            update_users = (update(u).where(u.id == user_id).values(is_verified=True))
            update_email = (update(e).where(e.user_id == user_id)).values(it_expired=True)
            sess.execute(update_users)
            sess.execute(update_email)
            sess.commit()
    def deactivate_old_code(self, user_id: int) -> list:
        try:
            with self.session as sess:
                e = aliased(EmailVerificationOrm)
                u = aliased(UsersOrm)
                token = sess.execute(select(e.token).select_from(e).join(u, e.user_id == u.id).where(u.id == user_id))
                request = delete(e).where(e.token == token)
                sess.execute(request)
                sess.commit()
                return [True, "The old code has been deleted"]
        except Exception as e:
            return [False, str(e)]

from models.orders import OrdersOrm
from models.verify_orders import OrdersVerificationOrm
class OrderVerifyRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_code(self, order_id: int, driver_id: int, code: int, token: str) -> bool:
        with self.session as sess:
            n_o_v_c = OrdersVerificationOrm(order_id= order_id, driver_id= driver_id, code= code, token= token, expires_at= ((datetime.now(UTC)) + timedelta(minutes=5)))
            sess.add(n_o_v_c)
            sess.commit()
            return True

    def select_code_data(self, order_token: str) -> OrdersVerificationOrm:
        with self.session as sess:
            query = select(OrdersVerificationOrm).select_from(OrdersVerificationOrm).where(OrdersVerificationOrm.token == order_token)
            code_data = sess.execute(query).scalars().first()
            return code_data

    def deactivate_code(self, token: str):
        with self.session as sess:
            update_query = update(OrdersVerificationOrm).where(OrdersVerificationOrm.token == token).values(it_expired=True)
            sess.execute(update_query)
            sess.commit()

    def verify_order(self, token: str) -> None:
        with self.session as sess:
            o = aliased(OrdersOrm)
            o_v = aliased(OrdersVerificationOrm)
            query_select = select(o_v.order_id).select_from(o_v).where(o_v.token == token)
            order_id = sess.execute(query_select).first()[0]
            query_update = update(o).where(o.id==order_id).values(status=OrderStatus.on_way)
            sess.execute(query_update)
            sess.commit()

from models.refresh_tokens import RefreshTokensOrm
class RefreshTokensRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_refresh_token(self, user_id: int, token_hash: str, expires_at: datetime, jti: str) -> tuple:
        with self.session as sess:
            new_ref_token = RefreshTokensOrm(user_id = user_id, token_hash=token_hash, expires_at=expires_at, jti=jti)
            sess.add(new_ref_token)
            sess.commit()
            return True,
    def get_token_data_by_user_id(self, user_id: int) -> RefreshTokensOrm:
        with self.session as sess:
            r = aliased(RefreshTokensOrm)
            query = select(r).select_from(r).where((r.user_id == user_id) & (r.is_revoked.is_(False)))
            data = sess.execute(query).scalars().first()
            return data


    def delete_token_data_by_user_id(self, user_id: int):
        with self.session as sess:
            query = delete(RefreshTokensOrm).where(RefreshTokensOrm.user_id == user_id)
            sess.execute(query)
            sess.commit()


    def get_token_data_by_jti(self, jti: str) -> RefreshTokensOrm:
        with self.session as sess:
            r = aliased(RefreshTokensOrm)
            query = select(r).select_from(r).where((r.jti == jti) & (r.is_revoked.is_(False)))
            data = sess.execute(query).scalars().first()
            return data


    def delete_token_data_by_jti(self, jti: str):
        with self.session as sess:
            query = delete(RefreshTokensOrm).where(RefreshTokensOrm.jti == jti)
            sess.execute(query)
            sess.commit()

    def revoke_token(self, jti: str):
        with self.session as sess:
            query = update(RefreshTokensOrm).where(RefreshTokensOrm.jti == jti).values(is_revoked = True)
            sess.execute(query)
            sess.commit()