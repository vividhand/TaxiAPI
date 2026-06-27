from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from repositories.user import UserRepositories
from schemas.users import NewUserSchema
from auth.utils import (hash_password, email_validate, password_validate, jwt_encode, jwt_decode,
                        create_access_token, create_refresh_token, hash_token, REFRESH_TOKEN_EXPIRE_DAYS, verify_token)
from auth.depends import (get_token, verify_auth_user, get_user_id, get_user_repositories,
                          get_email_ver_repositories, get_refresh_tokens_repositories, get_refresh_token, get_driver_repositories)
from services.send_email import send_email_to_verify, send_email_to_driver
from services.verify_email import verify_email
import secrets
from datetime import datetime, UTC, timedelta
from repositories.verification import EmailVerifyRepositories, RefreshTokensRepositories
from schemas.new_order import NewOrderSchema
from schemas.refresh_token import RefreshRequestSchemas
from repositories.driver import DriverRepositories
from fastapi.security import HTTPBearer
from repositories.order import OrderRepositories

rt = APIRouter(prefix="/taxi_api/users", tags=["User"])
http_bearer = HTTPBearer()

@rt.post("/register", summary="Sign up")
def register_user(user: NewUserSchema, back_task: BackgroundTasks, user_connect: UserRepositories = Depends(get_user_repositories)):
    checked_email = email_validate(user.email)
    checked_password = password_validate(user.password)
    if not checked_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is invalid!")
    if checked_password:
        hashed_password = hash_password(user.password)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is invalid!")

    if not (user_connect.add_user(full_name= user.fullname, email= user.email, password=str(hashed_password))[0]):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    token = secrets.token_urlsafe(32)
    back_task.add_task(send_email_to_verify, email= user.email, subject="Your confirmation code. The code is valid for 5 minutes.", token=token)


    return {"status": 200,
            "token": token}

@rt.post("/verify", summary="Verification user")
def verify_user(token: str, code: int, user_connect: UserRepositories = Depends(get_user_repositories),
                verify_connect: EmailVerifyRepositories = Depends(get_email_ver_repositories),
                refresh_connect: RefreshTokensRepositories = Depends(get_refresh_tokens_repositories)):
    if verify_email(token=token, input_code=code):
        user = user_connect.select_user_by_verification_token(token=token)
        user_data = user[1]
        expires_at = verify_connect.select_expired_time(token=token)
        if datetime.now(UTC) < expires_at:
            verify_connect.update_status(token=token)
            access_payload = {
                "sub": user_data.id,
                "is_verified": user_data.is_verified}

            refresh_payload = {
                "sub": user_data.id}

            access_token = create_access_token(access_payload)
            refresh_token = create_refresh_token(refresh_payload)
            refresh_connect.add_refresh_token(user_id= user_data.id, token_hash=hash_token(refresh_token), expires_at=(datetime.now(UTC)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)))
            return {"status": 200,
                    "message": "User has been created",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="Verification code has expired")
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid verification code")

@rt.post("/refresh", summary="Refresh access token")
def refresh_access_token(refresh_token: RefreshRequestSchemas, user_id: int = Depends(get_user_id),
                         refresh_connect: RefreshTokensRepositories = Depends(get_refresh_tokens_repositories),
                         user_connect: UserRepositories = Depends(get_user_repositories)):
    token_data = refresh_connect.get_token_data_by_user_id(user_id=user_id)[1]
    hashed_token = token_data[2]
    token_expires_at = token_data[3]
    if token_expires_at > datetime.now(UTC):
        if verify_token(token=refresh_token.refresh_token, hashed_token=hashed_token):
            user = user_connect.select_user_by_id(id= user_id)[1]
            is_verified = user.is_verified
            access_payload = {
                "sub": user_id,
                "is_verified": is_verified}
            new_access_token = create_access_token(payload=access_payload)
            return {
                "access_token": new_access_token,
                "token_type": 'bearer'
            }
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid refresh token")
    raise HTTPException(status_code=status.HTTP_410_GONE, detail="Refresh token has been expired")


@rt.post("/resend-verification-code", summary="Resend code")
def resend_code(email: str, back_task: BackgroundTasks, user_connect: UserRepositories = Depends(get_user_repositories),
                verify_email_connect: EmailVerifyRepositories = Depends(get_email_ver_repositories)):
    user = user_connect.select_user_by_email(email=email)
    if user[0]:
        user_data = user[1]
        if user_data.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already verified")
        verify_email_connect.deactivate_old_code(user_id= user_data.id)
        token = secrets.token_urlsafe(32)
        back_task.add_task(send_email_to_verify, email=user_data.email, subject="Your confirmation code. The code is valid for 5 minutes.", token=token)

        return {"status": 200,
                "token": token}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")


@rt.post("/login", summary="Sign on")
def login_user(user = Depends(verify_auth_user), refresh_conn: RefreshTokensRepositories = Depends(get_refresh_tokens_repositories)):
    user_payload = {
        "sub": user[0]["id"],
        "is_verified": user[0]["is_verified"]
    }
    print(user_payload)
    res = refresh_conn.delete_token_data_by_user_id(user_id=user[0]["id"])
    if res[0]:
        access_token = create_access_token(payload=user_payload)
        refresh_token = create_refresh_token(payload=user_payload)

        refresh_conn.add_refresh_token(user_id=user[0]["id"], token_hash=hash_token(access_token),
                                       expires_at=(datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)))

        return {"Message": f"User {user[0]["fullname"]} is logged in",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"}
    print(f"\n\n\n{res[1]}\n\n\n")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

@rt.get("/search-free-driver", summary="Find a free driver")
def search_driver():
    dr = DriverRepositories()
    data = dr.select_free_driver()
    if data[0]:
        return data[1]
    else:
        raise HTTPException(status_code=404, detail="Not found")

def get_user_from_token(token: bytes = Depends(get_token)):
    token_data = jwt_decode(token)
    return token_data

@rt.post("/create-new-order", summary="Create new order")
def create_order(order: NewOrderSchema, back_task: BackgroundTasks, token_data: dict = Depends(get_user_from_token)):
    conn_driver = DriverRepositories()
    driver = conn_driver.select_driver_by_fullname(order.driver_fullname)
    conn_user = UserRepositories()
    user = conn_user.select_user_by_email(token_data.get("email"))
    if user[0]:
        user_id = user[1][-1]
        if driver[0]:
            back_task.add_task(send_email_to_driver, driver[1][-1], token_data.get("fullname"), order.location)
            conn_order = OrderRepositories()
            conn_order.add_order(user_id=user_id, driver_id=driver[0])
            return {"status": 200,
                    "detail": "Order has been created"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
