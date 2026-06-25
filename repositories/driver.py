from core.setting import engine
from models.drivers import DriverOrm
from models.users import UsersOrm
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select

class DriverRepositories:
    def __init__(self):
        self.session = Session(engine)

    def select_free_driver(self) -> list:
        try:
            with self.session as sess:
                """select u.id, u.fullname, u.email, d.status, d.registration_date from users u join drivers d on d.id  = u.id where d.status = 'active'"""
                d = aliased(DriverOrm)
                u = aliased(UsersOrm)
                query = select(u.id, u.fullname, d.status, d.registration_date).select_from(u).join(d, d.id == u.id).where(d.status=="active")
                result = sess.execute(query).mappings().all()
                if result:
                    return [True, result]
                else:
                    return [False, "Not found"]

        except Exception as e:
            return [False, str(e)]

    def select_driver_status_by_id(self, driver_id: int) -> list:
        try:
            with self.session as sess:
                d = aliased(DriverOrm)
                u = aliased(UsersOrm)
                query = select(d.status).select_from(d).join(u, d.id == u.id).where(d.id == driver_id)
                result = sess.execute(query).first()
                if result:
                    return [True, result]
                else:
                    return [False, "Not found"]

        except Exception as e:
            return [False, str(e)]
    def select_driver_by_fullname(self, driver_fullname: str) -> list:
        try:
            with self.session as sess:
                d = aliased(DriverOrm)
                u = aliased(UsersOrm)
                query = select(u.id, u.email).select_from(u).join(d, d.id == u.id).where(u.fullname==driver_fullname)
                result = sess.execute(query).first()
                if result:
                    return [True, result]
                else:
                    return [False, "Not found"]
        except Exception as e:
            return [False, str(e)]

    def select_driver_data_by_id(self, driver_id: int) -> list:
        try:
            with self.session as sess:
                d = aliased(DriverOrm)
                u = aliased(UsersOrm)
                query = select(d.id, d.registration_date, d.status).select_from(d).join(u, d.id == u.id).where(d.id == driver_id)
                result = sess.execute(query).first()
                if result:
                    return [True, result]
                else:
                    return [False, "Not found"]
        except Exception as e:
            return [False, str(e)]
    def select_driver_data_by_email(self, driver_email: int) -> list:
        try:
            with self.session as sess:
                d = aliased(DriverOrm)
                u = aliased(UsersOrm)
                query = select(d.id, d.registration_date, d.status).select_from(d).join(u, d.id == u.id).where(d.id == driver_email)
                result = sess.execute(query).first()
                if result:
                    return [True, result]
                else:
                    return [False, "Not found"]
        except Exception as e:
            return [False, str(e)]


