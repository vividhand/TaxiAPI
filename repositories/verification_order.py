from datetime import datetime, UTC, timedelta
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from core.setting import engine, OrderStatus
from models import OrdersVerificationOrm, OrdersOrm

class OrderVerifyRepositories:
    def __init__(self):
        self.session = Session(engine)

    def add_code(self, order_id: int, driver_id: int, code: int, token: str) -> None:
        with self.session as sess:
            new_row = OrdersVerificationOrm(order_id= order_id, driver_id= driver_id, code= code, token= token, expires_at= ((datetime.now(UTC)) + timedelta(minutes=5)))
            sess.add(new_row)
            sess.commit()

    def select_code_data(self, order_token: str) -> OrdersVerificationOrm:
        with self.session as sess:
            request = select(OrdersVerificationOrm).select_from(OrdersVerificationOrm).where(OrdersVerificationOrm.token == order_token)
            response = sess.execute(request).scalars().first()
            return response

    def deactivate_code(self, token: str) -> None:
        with self.session as sess:
            request = update(OrdersVerificationOrm).where(OrdersVerificationOrm.token == token).values(it_expired=True)
            sess.execute(request)
            sess.commit()

    def verify_order(self, token: str) -> None:
        with self.session as sess:
            request_select = select(OrdersVerificationOrm.order_id).where(OrdersVerificationOrm.token == token)
            response = sess.execute(request_select).scalar_one_or_none()
            request_update = update(OrdersOrm).where(OrdersOrm.id==response).values(status=OrderStatus.on_way)
            sess.execute(request_update)
            sess.commit()
