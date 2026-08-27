from core.setting import engine
from models.drivers import DriverOrm
from models.users import UsersOrm
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional

class DriverRepositories:
    def __init__(self):
        self.session = Session(engine)

    def select_free_driver(self) -> Optional[UsersOrm, DriverOrm]:
        with self.session as sess:
            request = select(UsersOrm.id, UsersOrm.fullname, UsersOrm.email, DriverOrm.status, DriverOrm.registration_date).join(DriverOrm, DriverOrm.id == UsersOrm.id).where(DriverOrm.status=="active")
            response = sess.execute(request).mappings().all()
            return response

    def select_driver_status_by_id(self, driver_id: int):
        with self.session as sess:
            request = select(DriverOrm.status).select_from(DriverOrm).join(UsersOrm, DriverOrm.id == UsersOrm.id).where(DriverOrm.id == driver_id)
            response = sess.execute(request).first()
            return response

    def select_driver_data_by_id(self, driver_id: int) -> DriverOrm:
        with self.session as sess:
            request = select(DriverOrm.id, DriverOrm.registration_date, DriverOrm.status).select_from(DriverOrm).join(UsersOrm, DriverOrm.id == UsersOrm.id).where(DriverOrm.id == driver_id)
            response = sess.execute(request).scalars().first()
            return response

    def select_driver_data_by_email(self, driver_email: str) -> UsersOrm:
        with self.session as sess:
            request = select(UsersOrm).select_from(UsersOrm).join(DriverOrm, DriverOrm.id == UsersOrm.id).where(UsersOrm.email == driver_email)
            response = sess.execute(request).scalars().first()
            return response