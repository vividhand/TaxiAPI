from fastapi import APIRouter, HTTPException, Depends, status
from schemas.new_driver import DriverSchema
from repositories.admin import AdminsRepositories
from auth.depends import get_admin_status, get_admin_repositories
rt = APIRouter(prefix="/taxi_api/admins", tags=["Admins"])

@rt.post("/add_driver", tags=["Admins"], summary="Adding driver")
async def add_driver(schem: DriverSchema, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories)):
    result = admin_conn.add_driver(fullname= schem.fullname, email= schem.email)[0]
    if result:
        return {"status": status.HTTP_201_CREATED, "detail": "Driver has been added"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid fullname or email")


@rt.patch("/unban_driver", tags=["Admins"], summary="Unban driver")
def unban_driver(schem: DriverSchema, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories)):
    result = admin_conn.unban_driver(fullname= schem.fullname, email= schem.email)[0]
    if result:
        return "User has been unbanned"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid fullname or email")


@rt.patch("/ban_driver", tags=["Admins"], summary="Ban driver")
async def ban_driver(schem: DriverSchema, is_admin: bool = Depends(get_admin_status), admin_conn: AdminsRepositories = Depends(get_admin_repositories)):
    result = admin_conn.ban_driver(fullname= schem.fullname, email= schem.email)[0]
    if result:
        return "User has been banned"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid fullname or email")