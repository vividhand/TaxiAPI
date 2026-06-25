from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.new_driver import DriverSchema
from repositories.admin import AdminsRepositories
from auth.utils import jwt_decode
from jwt.exceptions import InvalidTokenError
from repositories.user import UserRepositories
rt = APIRouter(prefix="/taxi_api/admins", tags=["Admins"])

http_bearer = HTTPBearer()
def get_admin_status(cred: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = cred.credentials
    try:
        payload = jwt_decode(jwt_token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    conn = UserRepositories()
    user_role = conn.select_user_by_email(email=payload.get("email"))
    if user_role[-1][-1] == True:
        return user_role
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins")
@rt.post("/taxi_api/admin/add_driver", tags=["Admins"], summary="Adding driver")
async def add_driver(schem: DriverSchema, is_admin: bool = Depends(get_admin_status)):
    try:
        que = AdminsRepositories()
        que.add_driver(fullname= schem.fullname, email= schem.email)
        return "Driver has been added"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@rt.patch("/taxi_api/admin/unban_driver", tags=["Admins"], summary="Unban driver")
def unban_driver(schem: DriverSchema, is_admin: bool = Depends(get_admin_status)):
    try:
        que = AdminsRepositories()
        que.unBanDriver(fullname= schem.fullname, email= schem.email)
        return "User has been unbanned"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@rt.patch("/taxi_api/admin/ban_driver", tags=["Admins"], summary="Ban driver")
async def ban_driver(schem: DriverSchema, is_admin: bool = Depends(get_admin_status)):
    try:
        que = AdminsRepositories()
        que.BanDriver(fullname=schem.fullname, email=schem.email)
        return "Driver has been banned"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))