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


def verify_auth_user(email: str = Form(), password: str = Form()):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    conn = UserRepositories()
    res = conn.select_user(email=email)
    if res[0]:
        if verify_password(password, res[1][0]["password"]):
            return res[1]
        else:
            raise unauthed_exc
    elif not (res[0]) and res[1] == "Invalid email or password":
        raise unauthed_exc
    else:
        raise unauthed_exc

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