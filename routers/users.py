from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from auth.depends import (get_user_id, get_user_repositories,
                          get_driver_repositories, get_order_repositories, get_reviews_repositories)
from fastapi.security import HTTPBearer
from services import send_email_to_driver, verify_order
from schemas import NewOrderSchema
from repositories import OrderRepositories, DriverRepositories, UserRepositories, ReviewsRepositories
from core.setting import Rate

rt = APIRouter(prefix="/users", tags=["User"])
http_bearer = HTTPBearer()

@rt.get("/get-free-driver", summary="Get a free driver")
def get_free_driver(_: int = Depends(get_user_id), driver_connect: DriverRepositories = Depends(get_driver_repositories), reviews_conn: ReviewsRepositories = Depends(get_reviews_repositories)):
    free_drivers = driver_connect.select_free_driver()
    if free_drivers is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The list of drivers is empty")
    response_data = []
    for driver in free_drivers:
        driver_data= {"driver_id": driver.get("id"),
                      "driver_fullname": driver.get("fullname"),
                      "driver_email": driver.get("email"),
                      "driver_rate": reviews_conn.get_average_driver_rate(driver.get("id")),
                      "driver_status": driver.get("status"),
                      "driver_registration_date": driver.get("registration_date")}
        response_data.append(driver_data)
    return {"message": "Ok",
            "data": response_data}


@rt.get("/me")
def get_me(user_id: int = Depends(get_user_id), user_conn: UserRepositories = Depends(get_user_repositories)):
    user_data = user_conn.select_user_by_id(user_id=user_id)
    return {"message": f"User Data {user_data.fullname}",
            "data": user_data}


@rt.post("/create-new-order", summary="Create new order")
def create_order(order: NewOrderSchema, back_task: BackgroundTasks, user_id = Depends(get_user_id), driver_conn: DriverRepositories = Depends(get_driver_repositories),
                 order_connect: OrderRepositories = Depends(get_order_repositories),
                 user_connect: UserRepositories = Depends(get_user_repositories)):

    driver_data = driver_conn.select_driver_data_by_email(order.driver_email)
    user_data = user_connect.select_user_by_id(user_id=int(user_id))
    if driver_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")

    order_connect.add_order(user_id=user_id, driver_id=driver_data.id, location=order.location)
    order_id = order_connect.get_order_id(user_id=user_id, driver_id=driver_data.id, location= order.location)

    back_task.add_task(send_email_to_driver,order_id, driver_data.email, user_data.fullname, order.location)
    return {"message": "Order has been created",
            "data": {}}


@rt.post("/add-review")
def add_review(driver_email: str, order_id: int, text: str, user_id: int = Depends(get_user_id), rate: Rate = 1,
               review_conn: ReviewsRepositories = Depends(get_reviews_repositories),
               driver_conn: DriverRepositories = Depends(get_driver_repositories)):
    driver_data = driver_conn.select_driver_data_by_email(driver_email=driver_email)

    if not verify_order(order_id=order_id, driver_id=driver_data.id, user_id=int(user_id)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Order id or driver email is invalid")

    if not (review_conn.get_reviews_by_order_id(order_id=order_id) is None):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Review already exists")

    review_conn.add_review(user_id=user_id, driver_id=driver_data.id, order_id=order_id, rate=rate, text=text)
    return {"message": "Review has been added",
            "data": {}}

@rt.get("/my-reviews")
def get_reviews(user_id_: int = Depends(get_user_id), reviews_conn: ReviewsRepositories = Depends(get_reviews_repositories)):
    my_reviews = reviews_conn.get_reviews_by_user_id(user_id=user_id_)
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
    return {"message": "Ok",
            "data": response_data}
