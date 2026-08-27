from datetime import datetime, UTC
from core.setting import engine, OrderStatus
from sqlalchemy.orm import Session
from sqlalchemy import update, select
from models import OrdersOrm

class OrderRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_order(self, user_id: int, driver_id: int, location: str) -> None:
        with self.session as sess:
            new_order = OrdersOrm(user_id=user_id, driver_id=driver_id, location=location)
            sess.add(new_order)
            sess.commit()

    def update_status_order(self, order_id: int, order_status: OrderStatus) -> None:
        with self.session as sess:
            request = update(OrdersOrm).where(OrdersOrm.id == order_id).values(status=order_status, completed_at=datetime.now(UTC))
            sess.execute(request)
            sess.commit()

    def get_order_id(self, user_id: int, driver_id: int, location: str) -> int:
        with self.session as sess:
            request = select(OrdersOrm.id).select_from(OrdersOrm).where((OrdersOrm.user_id == user_id) & (OrdersOrm.driver_id == driver_id) & (OrdersOrm.location == location))
            response = sess.execute(request).mappings().first()
            return response["id"]

    def get_order_by_driver_id(self, driver_id: int) -> OrdersOrm:
        with self.session as sess:
            request = select(OrdersOrm).where((OrdersOrm.driver_id == driver_id) & (OrdersOrm.status.in_([OrderStatus.waiting, OrderStatus.on_way])))
            response = sess.execute(request).scalars().first()
            return response

    def get_order_by_id(self, order_id: int) -> OrdersOrm:
        with self.session as sess:
            request = select(OrdersOrm).where(OrdersOrm.id == order_id)
            response = sess.execute(request).scalars().first()
            return response