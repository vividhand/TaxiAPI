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
            query = update(OrdersOrm).where(OrdersOrm.id == order_id).values(status=order_status, completed_at=datetime.now(UTC))
            sess.execute(query)
            sess.commit()
    def get_order_id(self, user_id: int, driver_id: int, location: str) -> int:
        with self.session as sess:
            query = select(OrdersOrm.id).select_from(OrdersOrm).where((OrdersOrm.user_id == user_id) & (OrdersOrm.driver_id == driver_id) & (OrdersOrm.location == location))
            order_id = sess.execute(query).mappings().first()
            return order_id["id"]

    def get_order_by_driver_id(self, driver_id: int) -> OrdersOrm:
        with self.session as sess:
            query = select(OrdersOrm).where((OrdersOrm.driver_id == driver_id) & (OrdersOrm.status.in_([OrderStatus.waiting, OrderStatus.on_way])))
            orders = sess.execute(query).scalars().first()
            return orders
    def get_order_by_id(self, order_id: int) -> OrdersOrm:
        with self.session as sess:
            query = select(OrdersOrm).where(OrdersOrm.id == order_id)
            order = sess.execute(query).scalars().first()
            return order

# tert = OrderRepositories()
# order = tert.get_order_by_id(1)
# print(order.id, order.user_id, order.driver_id, order.location, order.date, order.status)