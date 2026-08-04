from fastapi import Depends, HTTPException, status
from repositories.user import UserRepositories
from repositories.driver import DriverRepositories
from auth.depends import get_user_id

def get_user_role(user_id = Depends(get_user_id)) -> dict:
    conn_to_user = UserRepositories()
    user_data = conn_to_user.select_user_by_id(user_id=int(user_id))
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    conn_to_driver = DriverRepositories()
    driver_data = conn_to_driver.select_driver_data_by_id(driver_id=user_id)
    if driver_data is None:
        return {"user_id": int(user_id), "role": "user"}
    return {"user_id": int(user_id), "role": "driver"}

