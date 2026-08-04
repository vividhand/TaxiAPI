from core.setting import engine, DriverStatus
from models import UsersOrm, DriverOrm
from sqlalchemy.orm import Session
from sqlalchemy import select, update

class AdminsRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_driver(self, email: str) -> bool:
        with self.session as sess:
            user_id_request = select(UsersOrm.id).where(UsersOrm.email == email)
            user_id = sess.execute(user_id_request).scalar_one_or_none()
            if user_id is None:
                return False
            new_driver = DriverOrm(id=user_id)
            sess.add(new_driver)
            sess.commit()
            return True

    def ban_driver(self, email: str) -> bool:
        with self.session as sess:
            user_id_request = select(UsersOrm.id).where(UsersOrm.email == email)
            user_id = sess.execute(user_id_request).scalar_one_or_none()
            if user_id is None:
                return False
            ban_request = (update(DriverOrm).where(DriverOrm.id == user_id).values(status=DriverStatus.banned))
            sess.execute(ban_request)
            sess.commit()
            return True

    def unban_driver(self, email: str) ->bool:
        with self.session as sess:
            user_id_request = select(UsersOrm.id).where(UsersOrm.email == email)
            user_id = sess.execute(user_id_request).scalar_one_or_none()
            if user_id is None:
                return False
            unban_request = (update(DriverOrm).where(DriverOrm.id == user_id).values(status=DriverStatus.active))
            sess.execute(unban_request)
            sess.commit()
            return True