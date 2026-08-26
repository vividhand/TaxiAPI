from datetime import datetime, UTC
from fastapi import APIRouter, HTTPException, Depends, status
from repositories import OrderVerifyRepositories, OrderRepositories, ReviewsRepositories
from services import get_user_role
from auth.depends import get_order_repositories, get_reviews_repositories, get_order_ver_repositories
from core.setting import OrderStatus

rt = APIRouter(tags=["Drivers"])

@rt.post("/verify_order")
def verify_order(order_token: str, code: int, role: dict = Depends(get_user_role), order_ver_conn: OrderVerifyRepositories = Depends(get_order_ver_repositories)):
    if role["role"] != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a driver")
    order_data = order_ver_conn.select_code_data(order_token=order_token)
    if order_data is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid order token")
    if order_data.it_expired:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code has been expired")
    if order_data.expires_at < datetime.now(UTC):
        order_ver_conn.deactivate_code(token=order_data.token)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code has been expired")
    if not (order_data.code == code):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid verification code")

    order_ver_conn.verify_order(token=order_token)
    order_ver_conn.deactivate_code(token=order_token)
    return {"message": "Order has been verified",
            "data": {}}

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
    order = order_conn.get_order_by_id(order_id=order_id)
    if order.status == OrderStatus.completed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already completed")
    order_conn.update_status_order(order_id=order_id, order_status=OrderStatus.completed)
    return {"message": "Ok",
            "detail": "Order has been completed"}

@rt.get("/my-reviews")
def get_reviews(reviews_conn: ReviewsRepositories = Depends(get_reviews_repositories), role: dict = Depends(get_user_role)):
    if role["role"] != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a driver")
    my_reviews = reviews_conn.get_reviews_by_driver_id(driver_id=role["user_id"])
    response_data = []
    for review in my_reviews:
        review_data = {"review_id": review.get("id"),
                      "order_id": review.get("order_id"),
                      "driver_id": review.get("driver_id"),
                      "user_id": review.get("user_id"),
                      "rate": review.get("rate"),
                       "text": review.get("text"),
                       "date": review.get("date")}
        response_data.append(review_data)
    return response_data