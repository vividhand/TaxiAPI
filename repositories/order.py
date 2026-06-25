from core.setting import engine
from models.orders import OrdersOrm
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from models.drivers import DriverOrm
from models.users import UsersOrm
from services.send_email import send_email_to_driver
class OrderRepositories:
    def __init__(self):
        self.session = Session(engine)
    def add_order(self, user_id: int, driver_id: int) -> list:
        try:
            with self.session as sess:
                new_order = OrdersOrm(user_id=user_id, driver_id=driver_id)
                select_driver_email = select(UsersOrm.email).select_from(UsersOrm).join(DriverOrm, UsersOrm.id == DriverOrm.id).where(DriverOrm.id == driver_id)
                email = sess.execute(select_driver_email).first()
                send_email_to_driver(email)
                sess.add(new_order)
                sess.commit()
                return [True, "Order has been created. Wait for confirmation from the driver"]
        except Exception as e:
            return [False, str(e)]

    def update_status_order(self, order_id: int, order_status: str) -> list:
        try:
            with self.session as sess:
                query = update(OrdersOrm).where(OrdersOrm.id == order_id).values(status=order_status)
                sess.execute(query)
                sess.commit()
                return [True, "Order`s status has been updated"]
        except Exception as e:
            return [False, str(e)]

    # def create_new_order(self, user_id: int, driver_id: int) -> list:
    #     try:
    #         with self.session as sess:
    #             new_order = OrdersOrm(user_id=user_id, driver_id=driver_id)
    #             sess.add(new_order)
    #             sess.commit()
    #             return [True, "Order has been created. Wait for confirmation from the driver"]
    #     except Exception as e:
    #         return [False, str(e)]
