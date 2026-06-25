from core.setting import engine
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, insert
from models.users import UsersOrm
from models.drivers import DriverOrm
from models.reviews import ReviewsOrm
class ReviewsRepositories:
    def __init__(self):
        self.session = Session(engine)
    def add_review(self, username: str, driver_name: str, rate: int, text: str):
        try:
            with self.session as sess:
                u = aliased(UsersOrm)
                d = aliased(DriverOrm)
                query_user = select(u.id).select_from(u).where(u.fullname == username)
                user_id = sess.execute(query_user).mappings().first()
                query_driver = select(d.id).select_from(d).join(u, d.id == u.id).where(u.fullname == u)
                driver_id = sess.execute(query_driver).mappings().first()
                review = ReviewsOrm(user_id= user_id,
                                    driver_id=driver_id,
                                    rate=rate,
                                    text=text)
                sess.add(review)
                sess.commit()
                return True
        except Exception as e:
            return [False, e]
