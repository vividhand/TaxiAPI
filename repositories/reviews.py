from core.setting import engine
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, func
from models import ReviewsOrm

class ReviewsRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_review(self, user_id: int, order_id: int, driver_id: str, rate: int, text: str) -> None:
        with self.session as sess:
            new_review = ReviewsOrm(order_id= order_id, driver_id=driver_id, user_id=user_id, rate=rate, text=text)
            sess.add(new_review)
            sess.commit()

    def get_reviews_by_user_id(self, user_id: int):
        with self.session as sess:
            r = aliased(ReviewsOrm)
            request = select(r.id, r.order_id, r.driver_id, r.user_id, r.rate, r.text, r.date).where(r.user_id == user_id)
            response = sess.execute(request).mappings().all()
            return response

    def get_reviews_by_driver_id(self, driver_id: int):
        with self.session as sess:
            r = aliased(ReviewsOrm)
            request = select(r.id, r.order_id, r.driver_id, r.user_id, r.rate, r.text, r.date).where(r.driver_id == driver_id)
            response = sess.execute(request).mappings().all()
            return response

    def get_reviews_by_order_id(self, order_id: int):
        with self.session as sess:
            request = select(ReviewsOrm).where(ReviewsOrm.order_id == order_id)
            response = sess.execute(request).scalars().first()
            return response

    def get_average_driver_rate(self, driver_id) -> float:
        with self.session as sess:
            request = select(func.avg(ReviewsOrm.rate)).where(ReviewsOrm.driver_id == driver_id)
            response = sess.execute(request).scalar()
            return response