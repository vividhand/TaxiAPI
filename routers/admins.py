from fastapi import APIRouter, HTTPException, Depends, status
from repositories.admin import AdminsRepositories
from auth.depends import get_admin_status, get_admin_repositories
rt = APIRouter(prefix="/admins", tags=["Admins"])

@rt.post("/add-driver", tags=["Admins"], summary="Adding driver")
async def add_driver(email: str, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories)):
    result = admin_conn.add_driver(email= email)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found or he is already created")
    return {"status": status.HTTP_201_CREATED, "detail": "Driver has been added"}


@rt.patch("/unban-driver", tags=["Admins"], summary="Unban driver")
def unban_driver(email: str, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories)):
    result = admin_conn.add_driver(email= email)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found or he is active")
    return {"status": status.HTTP_201_CREATED, "detail": "Driver has been unbanned"}


@rt.patch("/ban-driver", tags=["Admins"], summary="Ban driver")
async def ban_driver(email: str, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories)):
    result = admin_conn.add_driver(email= email)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found or he is already banned")
    return {"status": status.HTTP_201_CREATED, "detail": "Driver has been banned"}