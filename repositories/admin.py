from core.setting import engine
from models.drivers import DriverOrm
from models.users import UsersOrm
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, update



class AdminsRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_driver(self, fullname: str, email: str):
        try:
            with self.session as sess:
                u = aliased(UsersOrm)
                query = select(u.id).select_from(u).where(u.fullname == fullname and u.email == email)
                result = sess.execute(query).mappings().all()
                new_driver = DriverOrm(id=result[0]["id"])
                sess.add(new_driver)
                sess.commit()
                return True
        except Exception as e:
            return [False, e]

    def ban_driver(self, fullname: str, email: str):
        with self.session as sess:
            try:
                """update drivers d set status = 'banned' from users u where d.id = u.id and u.fullname = 'Ronoa Zoro' and u.email = 'god_of_the_hell@gmail.com';"""
                u = aliased(UsersOrm)
                d = aliased(DriverOrm)
                query_users = (select(u.id).select_from(u).where((u.fullname==fullname) & (u.email == email)))
                user_id = sess.execute(query_users).first()
                if user_id:
                    query = (update(d).where(d.id == user_id).values(status="banned"))
                    sess.execute(query)
                    sess.commit()
                    return True
                else:
                    return [False, "Driver not found"]
            except Exception as e:
                return [False, e]

    def unban_driver(self, fullname: str, email: str):
        with self.session as sess:
            try:
                """update drivers d set status = 'banned' from users u where d.id = u.id and u.fullname = 'Ronoa Zoro' and u.email = 'god_of_the_hell@gmail.com';"""
                u = aliased(UsersOrm)
                d = aliased(DriverOrm)
                query_users = (select(u.id).select_from(u).where((u.fullname == fullname) & (u.email == email)))
                result_users = sess.execute(query_users).mappings().all()
                if result_users:
                    user_id = result_users[0]["id"]
                    query = (update(d).where(d.id == user_id).values(status="active"))
                    sess.execute(query)
                    sess.commit()
                    return True
                else:
                    return [False, "Driver not found"]
            except Exception as e:
                return [False, e]


