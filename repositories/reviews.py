from core.setting import engine
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, func
from models import ReviewsOrm

class ReviewsRepositories:
    def __init__(self):
        self.session = Session(engine)
    def add_review(self, user_id: int, order_id: int, driver_id: str, rate: int, text: str):
        with self.session as sess:
            new_review = ReviewsOrm(order_id= order_id, driver_id=driver_id, user_id=user_id, rate=rate, text=text)
            sess.add(new_review)
            sess.commit()

    def delete_review(self, user_id: int, order_id: int):
        with self.session as sess:
            delete_review = delete(ReviewsOrm).where((ReviewsOrm.user_id == user_id) & (ReviewsOrm.order_id == order_id))
            sess.execute(delete_review)
            sess.commit()
    def get_reviews_by_user_id(self, user_id: int):
        with self.session as sess:
            select_review = select(ReviewsOrm).where(ReviewsOrm.user_id == user_id)
            reviews = sess.execute(select_review).scalars().first()
            return reviews

    def get_reviews_by_driver_id(self, driver_id: int):
        with self.session as sess:
            select_review = select(ReviewsOrm).where(ReviewsOrm.driver_id == driver_id)
            reviews = sess.execute(select_review).scalars().first()
            return reviews

    def get_reviews_by_order_id(self, order_id: int):
        with self.session as sess:
            select_review = select(ReviewsOrm).where(ReviewsOrm.order_id == order_id)
            reviews = sess.execute(select_review).scalars().first()
            return reviews

    def get_average_driver_rate(self, driver_id) -> float:
        with self.session as sess:
            query = select(func.avg(ReviewsOrm.rate)).where(ReviewsOrm.driver_id == driver_id)
            avg_rate = sess.execute(query).scalar()
            return avg_rate


# rrt = ReviewsRepositories()
# print(rrt.get_reviews_by_user_id(3).text)
# print(rrt.get_reviews_by_driver_id(4).rate)
# print(rrt.get_reviews_by_order_id(1).date)