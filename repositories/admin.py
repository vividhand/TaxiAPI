from core.setting import engine, DriverStatus
from models import UsersOrm, DriverOrm
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from typing import Optional

class AdminsRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_driver(self, fullname: str, email: str) -> tuple[bool, Optional[str, None]]:
        with self.session as sess:
            query_user_id = select(UsersOrm.id).select_from(UsersOrm).where((UsersOrm.fullname == fullname) & (UsersOrm.email == email))
            user_id = sess.execute(query_user_id).first()
            if user_id:
                new_driver = DriverOrm(id=user_id)
                sess.add(new_driver)
                sess.commit()
                return True, "Driver has been added"
            return False, None

    def ban_driver(self, fullname: str, email: str) -> tuple[bool, Optional[str, None]]:
        with self.session as sess:
            query_user_id = (select(UsersOrm.id).select_from(UsersOrm).where((UsersOrm.fullname==fullname) & (UsersOrm.email == email)))
            user_id = sess.execute(query_user_id).first()
            if user_id:
                query = (update(DriverOrm).where(DriverOrm.id == user_id).values(status=DriverStatus.banned))
                sess.execute(query)
                sess.commit()
                return True, None
            else:
                return False, "Driver not found"

    def unban_driver(self, fullname: str, email: str) -> tuple[bool, Optional[str, None]]:
        with self.session as sess:
            query_user_id = (select(UsersOrm.id).select_from(UsersOrm).where((UsersOrm.fullname==fullname) & (UsersOrm.email == email)))
            user_id = sess.execute(query_user_id).first()
            if user_id:
                query = (update(DriverOrm).where(DriverOrm.id == user_id).values(status=DriverStatus.active))
                sess.execute(query)
                sess.commit()
                return True, None
            else:
                return False, "Driver not found"


