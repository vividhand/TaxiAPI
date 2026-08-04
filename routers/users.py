from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from auth.depends import (get_user_id, get_user_repositories,
                          get_driver_repositories, get_order_repositories, get_reviews_repositories)
from fastapi.security import HTTPBearer
from services import send_email_to_driver, verify_order
from schemas import NewOrderSchema, UserSchema
from repositories import OrderRepositories, DriverRepositories, UserRepositories, ReviewsRepositories
from core.setting import Rate

rt = APIRouter(prefix="/users", tags=["User"])
http_bearer = HTTPBearer()


@rt.get("/search-free-driver", summary="Find a free driver")
def search_driver(driver_connect: DriverRepositories = Depends(get_driver_repositories), reviews_conn: ReviewsRepositories = Depends(get_reviews_repositories)):
    free_drivers = driver_connect.select_free_driver()
    if free_drivers is None:
        return {"Drivers": "Not Found"}
    return free_drivers

@rt.get("/average-rate_driver")
def get_avg_rate(driver_id: int, review_conn: None):
    pass

@rt.get("/me")
def get_me(user_id: int = Depends(get_user_id), user_conn: UserRepositories = Depends(get_user_repositories)):
    user_data = user_conn.select_user_by_id(user_id=user_id)
    return {"message": f"User Data {user_data.fullname}",
            "data": user_data}


@rt.post("/create-new-order", summary="Create new order")
def create_order(order: NewOrderSchema, back_task: BackgroundTasks, user_id = Depends(get_user_id), driver_conn: DriverRepositories = Depends(get_driver_repositories),
                 order_connect: OrderRepositories = Depends(get_order_repositories),
                 user_connect: UserRepositories = Depends(get_user_repositories)):

    driver_data = driver_conn.select_driver_by_fullname(order.driver_fullname)
    user_data = user_connect.select_user_by_id(user_id=int(user_id))
    if driver_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    order_connect.add_order(user_id=user_id, driver_id=driver_data.id, location=order.location)
    order_id = order_connect.get_order_id(user_id=user_id, driver_id=driver_data.id, location= order.location)

    back_task.add_task(send_email_to_driver,order_id, driver_data.email , user_data.fullname, order.location)
    return {"status": 200,
            "detail": "Order has been created"}


@rt.post("/add-review")
def add_review(driver_fullname: str, order_id: int, text: str, user_id: int = Depends(get_user_id), rate: Rate = 1,
               review_conn: ReviewsRepositories = Depends(get_reviews_repositories),
               driver_conn: DriverRepositories = Depends(get_driver_repositories)):
    driver_data = driver_conn.select_driver_by_fullname(driver_fullname=driver_fullname)
    if verify_order(order_id=order_id, driver_id=driver_data.id, user_id=user_id):
        review_conn.add_review(user_id=user_id, driver_id=driver_data.id, order_id=order_id, rate=rate, text=text)
        return {"message": "Ok",
                "detail": "Review has been added"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@rt.get("/my-reviews")
def get_reviews(user_id_: int = Depends(get_user_id), reviews_conn: ReviewsRepositories = Depends(get_reviews_repositories)):
    my_reviews = reviews_conn.get_reviews_by_user_id(user_id=user_id_)
    return my_reviews
