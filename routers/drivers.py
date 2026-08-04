from datetime import datetime, UTC
from fastapi import APIRouter, HTTPException, Depends, status
from repositories import OrderVerifyRepositories, OrderRepositories, ReviewsRepositories
from services.get_user_role import get_user_role
from auth.depends import get_user_id, get_order_repositories, get_reviews_repositories
from core.setting import OrderStatus

rt = APIRouter(tags=["Drivers"])

@rt.post("/verify_order")
def verify_order(order_token: str, code: int, role: dict = Depends(get_user_role)):
    if role["role"] != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a driver")
    conn = OrderVerifyRepositories()
    order_data = conn.select_code_data(order_token=order_token)
    if order_data is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid order token")
    if order_data.it_expired and order_data.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code has been expired")
    if order_data.code == code:
        conn.verify_order(token=order_token)
        conn.deactivate_code(token=order_token)
        return {"status": 200,
                "message": "Order has been verified."}
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid verification code")

@rt.get("/get-active-order")
def get_active_order(order_conn: OrderRepositories = Depends(get_order_repositories), role: dict = Depends(get_user_role)):
    if role["role"] != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a driver")
    orders = order_conn.get_order_by_driver_id(driver_id=role["user_id"])
    return orders

@rt.post("/complete-order")
def complete_order(order_id: int, order_conn: OrderRepositories = Depends(get_order_repositories), role: dict = Depends(get_user_role)):
    if role["role"] != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a driver")
    order_conn.update_status_order(order_id=order_id, order_status=OrderStatus.completed)
    return {"message": "Ok",
            "detail": "Order has been completed"}

@rt.get("/my-reviews")
def get_reviews(reviews_conn: ReviewsRepositories = Depends(get_reviews_repositories), role: dict = Depends(get_user_role)):
    if role["role"] != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a driver")
    my_reviews = reviews_conn.get_reviews_by_user_id(user_id=role["id"])
    return my_reviews