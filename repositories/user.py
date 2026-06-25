from core.setting import engine
from models.users import UsersOrm
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, text
from models.verify_email import EmailVerificationOrm
from models.orders import OrdersOrm
from models.drivers import DriverOrm
class UserRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_user(self, full_name: str, email: str, password: str) -> list:
        try:
            with self.session as sess:
                try:
                    new_user = UsersOrm(fullname=full_name, email=email, password=password)
                    sess.add(new_user)
                    sess.commit()
                    return [True, "User has been added"]
                except Exception:
                    sess.rollback()
                    return [False, "Email already uses"]
        except Exception as e:
            return [False, str(e)]

    def select_user(self, email: str, password: str | None = None) -> list:
        try:
            with self.session as sess:
                if not (password is None):
                    query = select(text("*")).select_from(UsersOrm).filter_by(email=email, password=password)
                    result = sess.execute(query).mappings().all()
                    if result:
                        return [True, result]
                    else:
                        return [False, "Invalid email or password"]
                else:
                    query = select(text("*")).select_from(UsersOrm).filter_by(email=email)
                    result = sess.execute(query).mappings().all()
                    if result:
                        return [True, result]
                    else:
                        return [False, "Invalid email or password"]
        except Exception as e:
            return [False, str(e)]
    def select_user_by_verification_token(self, token: str) -> list:
        try:
            with self.session as sess:
                print(1)
                u = aliased(UsersOrm)
                e = aliased(EmailVerificationOrm)
                print(1.1)
                query = select(text("*")).select_from(u).join(e, e.user_id == u.id).where(e.token == token)
                print(1.2)
                user = sess.execute(query).mappings()
                print(f"User data: {user}")
                if user:
                    print(f"User data: {user}")
                    return [True, UsersOrm(id = user["id"], fullname=user["fullname"],
                                           email=user["email"], registration_date=user["registration_date"],
                                           is_admin=user["is_Admin"], is_verified = user["is_verified"])]
                else:
                    print(2)
                    return [False, "Invalid token"]
        except Exception as e:
            return [False, str(e)]

    def select_user_by_email(self, email: str) -> list:
        try:
            with self.session as sess:
                u = aliased(UsersOrm)
                query = select(u.id, u.fullname, u.email, u.is_admin, u.is_verified).select_from(u).where(u.email == email)
                user = sess.execute(query).first()
                print(user)
                if user:
                    return [True, user]
                else:
                    return [False, "Invalid email"]
        except Exception as e:
            return [False, str(e)]

    def select_user_by_id(self, user_id: int) -> list:
        try:
            with self.session as sess:
                u = aliased(UsersOrm)
                query = select(u.id, u.fullname, u.email, u.is_admin, u.is_verified,).select_from(u).where(u.id == user_id)
                user = sess.execute(query).first()
                print(user)
                if user:
                    return [True, user]
                else:
                    return [False, "Invalid id"]
        except Exception as e:
            return [False, str(e)]






