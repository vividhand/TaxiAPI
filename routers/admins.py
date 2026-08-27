from fastapi import APIRouter, HTTPException, Depends, status
from repositories import AdminsRepositories, DriverRepositories, UserRepositories
from auth.depends import get_admin_status, get_admin_repositories, get_driver_repositories, get_user_repositories
from core.setting import DriverStatus

rt = APIRouter(prefix="/admins", tags=["Admins"])

@rt.post("/add-driver", tags=["Admins"], summary="Adding driver")
def add_driver(email: str, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories),
                     driver_conn: DriverRepositories = Depends(get_driver_repositories),
                     user_conn: UserRepositories = Depends(get_user_repositories)):
    driver = driver_conn.select_driver_data_by_email(driver_email=email)
    if not (driver is None):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Driver already exists")
    user = user_conn.select_user_by_email(email=email)
    admin_conn.add_driver(user_id= user.id)
    return {"message": "Driver has been added",
            "data": {}}

@rt.patch("/unban-driver", tags=["Admins"], summary="Unban driver")
def unban_driver(email: str, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories),
                 driver_conn: DriverRepositories = Depends(get_driver_repositories)):
    driver = driver_conn.select_driver_data_by_email(driver_email=email)
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    driver_status = driver_conn.select_driver_status_by_id(driver_id=driver.id)
    if driver_status[0] is DriverStatus.active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Driver already active")
    admin_conn.unban_driver(driver_id=driver.id)
    return {"message": "Driver has been unbanned",
            "data": {}}

@rt.patch("/ban-driver", tags=["Admins"], summary="Ban driver")
def ban_driver(email: str, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories),
                     driver_conn: DriverRepositories = Depends(get_driver_repositories)):
    driver = driver_conn.select_driver_data_by_email(driver_email=email)
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    driver_status = driver_conn.select_driver_status_by_id(driver_id=driver.id)
    if driver_status[0] is DriverStatus.banned:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Driver already banned")
    admin_conn.ban_driver(driver_id= driver.id)
    return {"message": "Driver has been banned",
            "data": {}}