from fastapi import Depends, HTTPException, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from auth.utils import jwt_decode, verify_password
from repositories import (UserRepositories, AdminsRepositories, EmailVerifyRepositories, OrderVerifyRepositories,
                          RefreshTokensRepositories, DriverRepositories, OrderRepositories, ReviewsRepositories)
from schemas.tokens import RefreshRequestSchemas


http_bearer = HTTPBearer()

def get_token(cred: HTTPAuthorizationCredentials = Depends(http_bearer)):
    return cred.credentials

def get_user_data(token: str = Depends(get_token)):
    try:
        data = jwt_decode(token)
        return data
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

def get_user_id(data = Depends(get_user_data)):
    return data["sub"]

def verify_authorization(data = Depends(get_user_data)):
    if data["is_verified"]:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email is not verified")


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

def get_order_repositories():
    return OrderRepositories()
def get_refresh_tokens_repositories():
    return RefreshTokensRepositories()

def get_reviews_repositories():
    return ReviewsRepositories()

def get_refresh_token(body: RefreshRequestSchemas):
    return body.refresh_token
def verify_auth_user(email: str = Form(), password: str = Form(), user_conn: UserRepositories = Depends(get_user_repositories)):
    result = user_conn.select_user_by_email(email=email)
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if verify_password(password, str(result.password)):
        return result
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

def get_admin_status(user_id: str = Depends(get_user_id), user_conn: UserRepositories = Depends(get_user_repositories)):
    user_data = user_conn.select_user_by_id(int(user_id))
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    is_admin = user_data.is_admin
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins")
    return True