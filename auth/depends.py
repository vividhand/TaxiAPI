from fastapi import Depends, HTTPException, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from auth.utils import jwt_decode, verify_password
from repositories.user import UserRepositories
from repositories.admin import AdminsRepositories
from repositories.car import CarRepositories
from repositories.driver import DriverRepositories
from repositories.reviews import ReviewsRepositories
from repositories.verification import EmailVerifyRepositories, OrderVerifyRepositories, RefreshTokensRepositories
from repositories.order import OrderRepositories
from schemas.refresh_token import RefreshRequestSchemas
http_bearer = HTTPBearer()
from schemas.users import UserSchema


def get_token(cred: HTTPAuthorizationCredentials = Depends(http_bearer)):
    return cred.credentials


def get_user_data(token: str = Depends(get_token)):
    data = jwt_decode(token)
    return data

def get_user_id(data = Depends(get_user_data)):
    return data["id"]

def verify_authorization(data = Depends(get_user_data)):
    if data["is_verified"] == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email is not verified")
    return True


def get_admin_repositories():
    return AdminsRepositories()

def get_user_repositories():
    return UserRepositories()

def get_driver_repositories():
    return DriverRepositories()

def get_email_ver_repositories():
    return EmailVerifyRepositories()

def get_order_ver_repositories():
    return OrderVerifyRepositories()

def get_refresh_tokens_repositories():
    return RefreshTokensRepositories()

def get_refresh_token(body: RefreshRequestSchemas):
    return body.refresh_token

def verify_auth_user(email: str = Form(), password: str = Form(), user_conn: UserRepositories = Depends(get_user_repositories)):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    result = user_conn.select_user_by_email(email=email)
    if result[0]:
        user_data = result[1]
        if verify_password(password, user_data.password):
            return UserSchema.model_validate(user_data).model_dump()
        else:
            raise unauthed_exc
    else:
        raise unauthed_exc

def get_admin_status(payload: dict = Depends(get_user_data), user_conn: UserRepositories = Depends(get_user_repositories)):
    user = user_conn.select_user_by_email(email=payload.get("email"))
    user_data = user[1]
    is_admin = user_data.is_admin
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins")