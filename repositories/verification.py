from core.setting import engine
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, update,delete, Text
from models.users import UsersOrm
from models.verify_email import EmailVerificationOrm
from datetime import datetime, timedelta, UTC
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
    def select_verify_code(self, token):
        try:
            with self.session as sess:
                e = aliased(EmailVerificationOrm)
                request = select(e.code).select_from(e).where(e.token == token)
                code = sess.execute(request).first()
                return code
        except Exception as e:
            return [False, e]

    def select_expired_time(self, token):
        try:
            with self.session as sess:
                e = aliased(EmailVerificationOrm)
                expired_time = sess.execute(select(e.expires_at).select_from(e).where(e.token == token)).scalar_one()
                return expired_time
        except Exception as e:
            return [False, e]
    def update_status(self, token: str):
        try:
            with self.session as sess:
                e = aliased(EmailVerificationOrm)
                u = aliased(UsersOrm)
                user_id_request = select(u.id).select_from(u).join(e, e.user_id == u.id).where(e.token == token)
                user_id = sess.execute(user_id_request).first()
                update_request = (update(u).where(u.id == user_id[0]).values(is_verified=True))
                sess.execute(update_request)
                sess.commit()
                return True
        except Exception as e:
            return [False, e]
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

    def add_code(self, driver_id: int, code: int, token: str) -> list:
        with self.session as sess:
            try:
                now = datetime.now(UTC)
                new_order_ver_row = OrdersVerificationOrm(driver_id=driver_id, code=code, token=token, expired_at=(now+timedelta(minutes=5)))
                sess.execute(new_order_ver_row)
                sess.commit()
                return [True, "Order verification row has been created"]
            except Exception as e:
                return [False, str(e)]
    def select_code(self, order_token: str) -> list:
        with self.session as sess:
            try:
                o = aliased(OrdersVerificationOrm)
                query = select(o.order_id, o.driver_id, o.code, o.token, o.expires_at, o.driver_id).select_from(o).where(o.token == order_token)
                order_data = sess.execute(query).first()
                if order_data:
                    return [True, order_data]
                return [False, "Not found"]
            except Exception as e:
                return [False, str(e)]
    def verify_order(self, token: str) -> list:
        with self.session as sess:
            try:
                o = aliased(OrdersOrm)
                o_v = aliased(OrdersVerificationOrm)
                query_select = select(o_v.order_id).select_from(o_v).where(o_v.token==token)
                order_id = sess.execute(query_select).first()[0]
                if order_id:
                    query_update = update(o).where(o.id==order_id).values(status="on_way")
                    sess.execute(query_update)
                    sess.commit()
                    return [True, "Order has been verified"]
                return [False, "Invalid token"]
            except Exception as e:
                return [False, str(e)]

from models.refresh_tokens import RefreshTokensOrm
class RefreshTokensRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_refresh_token(self, user_id: int, token_hash: str, expires_at: datetime) -> list:
        with self.session as sess:
            try:
                new_ref_token = RefreshTokensOrm(user_id = user_id, token_hash=token_hash, expires_at=expires_at)
                sess.execute(new_ref_token)
                sess.commit()
                return [True, "Token has been added"]
            except Exception as e:
                return [False, str(e)]
    def get_token_data_by_user_id(self, user_id: int) -> list:
        with self.session as sess:
            try:
                r = aliased(RefreshTokensOrm)
                query = select(r.id, r.user_id, r.token_hash, r.expires_at, r.is_revoked).select_from(r).where(r.user_id == user_id, r.is_revoked.is_(False))
                data = sess.execute(query).mappings().first()
                return [True, data]
            except Exception as e:
                return [False, str(e)]

    def delete_token_data_by_user_id(self, user_id: int) -> list:
        with self.session as sess:
            try:
                r = aliased(RefreshTokensOrm)
                query = delete(r).where(r.user_id == user_id)
                sess.execute(query)
                sess.commit()
                return [True, "Token data has been deleted"]
            except Exception as e:
                return [False, str(e)]