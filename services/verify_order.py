from repositories import OrderRepositories
from core.setting import OrderStatus
from datetime import datetime, UTC, timedelta

def verify_order(order_id: int, driver_id: int, user_id: int) -> bool:
    order_conn = OrderRepositories()
    order = order_conn.get_order_by_id(order_id=order_id)
    if order is None:
        return False
    user_id_or, driver_id_or = order.user_id, order.driver_id
    if (user_id_or == user_id) and (driver_id_or == driver_id) and (order.status == OrderStatus.completed) and ((datetime.now(UTC) - order.completed_at) < timedelta(hours=72)):
        return True
    return False
#
# print(verify_order(2, 4, 3))


