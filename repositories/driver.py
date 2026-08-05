from core.setting import engine
from models.drivers import DriverOrm
from models.users import UsersOrm
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select
from typing import Optional


class DriverRepositories:
    def __init__(self):
        self.session = Session(engine)

    def select_free_driver(self) -> Optional[UsersOrm, DriverOrm]:
        with self.session as sess:
            d = aliased(DriverOrm)
            u = aliased(UsersOrm)
            query = select(u.id, u.fullname, u.email, d.status, d.registration_date).select_from(u).join(d, d.id == u.id).where(d.status=="active")
            result = sess.execute(query).mappings().all()
            return result

    def select_driver_status_by_id(self, driver_id: int) -> Optional[UsersOrm, DriverOrm]:
        with self.session as sess:
            d = aliased(DriverOrm)
            u = aliased(UsersOrm)
            query = select(d.status).select_from(d).join(u, DriverOrm.id == UsersOrm.id).where(DriverOrm.id == driver_id)
            result = sess.execute(query).first()
            return result

    def select_driver_by_fullname(self, driver_fullname: str) -> Optional[UsersOrm, DriverOrm]:
        with self.session as sess:
            d = aliased(DriverOrm)
            u = aliased(UsersOrm)
            query = select(u).select_from(u).join(d, d.id == u.id).where(u.fullname==driver_fullname)
            result = sess.execute(query).scalars().first()
            return result

    def select_driver_data_by_id(self, driver_id: int) -> Optional[UsersOrm, DriverOrm]:
        with self.session as sess:
            d = aliased(DriverOrm)
            u = aliased(UsersOrm)
            query = select(d.id, d.registration_date, d.status).select_from(d).join(u, d.id == u.id).where(d.id == driver_id)
            result = sess.execute(query).scalars().first()
            return result
    def select_driver_data_by_email(self, driver_email: str) -> Optional[UsersOrm, DriverOrm]:
        with self.session as sess:
            query = select(UsersOrm).select_from(UsersOrm).join(DriverOrm, DriverOrm.id == UsersOrm.id).where(UsersOrm.email == driver_email)
            result = sess.execute(query).scalars().first()
            return result