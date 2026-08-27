from core.setting import engine, DriverStatus
from models import DriverOrm
from sqlalchemy.orm import Session
from sqlalchemy import update

class AdminsRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_driver(self, user_id: int) -> None:
        with self.session as sess:
            new_driver = DriverOrm(id= user_id)
            sess.add(new_driver)
            sess.commit()

    def ban_driver(self, driver_id: int) -> None:
        with self.session as sess:
            request = update(DriverOrm).where(DriverOrm.id == driver_id).values(status= DriverStatus.banned)
            sess.execute(request)
            sess.commit()

    def unban_driver(self, driver_id: int) -> None:
        with self.session as sess:
            request = update(DriverOrm).where(DriverOrm.id == driver_id).values(status= DriverStatus.active)
            sess.execute(request)
            sess.commit()