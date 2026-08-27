import secrets
import uuid
from datetime import datetime, UTC, timedelta
import jwt
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Cookie, Response
from starlette import status
from auth.depends import get_user_repositories, get_email_ver_repositories, get_refresh_tokens_repositories, \
    verify_auth_user
from auth.utils import email_validate, password_validate, hash_password, create_access_token, create_refresh_token, \
    hash_token, REFRESH_TOKEN_EXPIRE_DAYS, jwt_decode, REFRESH_TOKEN_TYPE, verify_token
from repositories import UserRepositories, EmailVerifyRepositories, RefreshTokensRepositories
from schemas import NewUserSchema
from services import send_email_to_verify, verify_email

rt = APIRouter(prefix="/auth", tags=["Authorization"])


@rt.post("/register", summary="Sign up")
def register_user(user: NewUserSchema, back_task: BackgroundTasks, user_connect: UserRepositories = Depends(get_user_repositories)):
    checked_email = email_validate(user.email)
    checked_password = password_validate(user.password)
    if (not checked_email) or (not checked_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or password is invalid")
    hashed_password = hash_password(user.password)
    if user_connect.select_user_by_email(email=user.email) is None:
        user_connect.add_user(full_name=user.fullname, email=user.email, password=hashed_password)
        token = secrets.token_urlsafe(32)
        back_task.add_task(send_email_to_verify, email=user.email, subject="Your confirmation code. The code is valid for 5 minutes.", token=token)

        return {"message": "User has been created",
                "data": {"token": token}}
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


@rt.post("/verify", summary="Verification user")
def verify_user(token: str, code: int, response: Response, user_connect: UserRepositories = Depends(get_user_repositories),
                verify_connect: EmailVerifyRepositories = Depends(get_email_ver_repositories),
                refresh_connect: RefreshTokensRepositories = Depends(get_refresh_tokens_repositories)):

    if not (verify_email(token=token, input_code=code)):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid verification code or token")

    user_data = user_connect.select_user_by_verification_token(token=token)
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid verification code or token")

    if user_data.is_verified:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already verified")

    expires_at = verify_connect.select_expired_time(token=token)
    if datetime.now(UTC) > expires_at:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Verification code has expired")

    verify_connect.update_status(token=token)
    jti = str(uuid.uuid4())
    access_payload = {
        "sub": str(user_data.id),
        "is_verified": user_data.is_verified}
    refresh_payload = {
        "sub": str(user_data.id),
        "jti": jti}
    access_token = create_access_token(access_payload)
    refresh_token = create_refresh_token(refresh_payload)
    refresh_connect.add_refresh_token(user_id= user_data.id, token_hash=hash_token(refresh_token), expires_at=(datetime.now(UTC)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)), jti=jti)
    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        httponly=True,
                        samesite="strict",
                        secure=False,
                        max_age=60*60*24*30,
                        path="/auth/refresh"
                        )
    return {"message": "User has been verified",
            "data": {"access_token": access_token, "token_type": "bearer"}}

@rt.post("/resend-verification-code", summary="Resend code")
def resend_code(email: str, back_task: BackgroundTasks, user_connect: UserRepositories = Depends(get_user_repositories),
                verify_email_connect: EmailVerifyRepositories = Depends(get_email_ver_repositories)):
    user_data = user_connect.select_user_by_email(email=email)
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")
    if user_data.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already verified")
    verify_email_connect.deactivate_old_code(user_id= user_data.id)
    token = secrets.token_urlsafe(32)
    back_task.add_task(send_email_to_verify, email=user_data.email, subject="Your confirmation code. The code is valid for 5 minutes.", token=token)

    return {"message": "New verification token",
            "data": {"token": token}}

@rt.post("/refresh", summary="Refresh access token")
def refresh_access_token(response: Response, refresh_token: str | None = Cookie(default=None),
                         refresh_connect: RefreshTokensRepositories = Depends(get_refresh_tokens_repositories),
                         user_connect: UserRepositories = Depends(get_user_repositories)):

    unauthorized_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if refresh_token is None:
        raise unauthorized_error

    try:
        decoded_token = jwt_decode(refresh_token)
    except jwt.PyJWTError:
        raise  unauthorized_error

    if decoded_token.get("type") != REFRESH_TOKEN_TYPE:
        raise unauthorized_error

    token_data = refresh_connect.get_token_data_by_jti(jti=decoded_token.get("jti"))
    if token_data is None:
        raise unauthorized_error

    if token_data.expires_at < datetime.now(UTC):
         raise unauthorized_error

    if token_data.is_revoked:
        raise unauthorized_error

    if not (verify_token(token=refresh_token, hashed_token=token_data.token_hash)):
        raise unauthorized_error


    user_data = user_connect.select_user_by_id(user_id=token_data.user_id)

    access_payload = {
        "sub": str(user_data.id),
        "is_verified": user_data.is_verified}
    jti = str(uuid.uuid4())
    refresh_payload = {
        "sub": str(user_data.id),
        "jti": jti}
    refresh_connect.revoke_token(jti=token_data.jti)

    new_access_token = create_access_token(payload=access_payload)
    new_refresh_token = create_refresh_token(payload=refresh_payload)
    refresh_connect.add_refresh_token(user_id=token_data.user_id, token_hash=hash_token(new_refresh_token), expires_at=(datetime.now(UTC)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)),jti=jti)
    response.set_cookie(key="refresh_token",
                        value=new_refresh_token,
                        httponly=True,
                        samesite="strict",
                        secure=False,
                        max_age=60*60*24*30,
                        path="/auth/refresh")

    return {"message": "Access token has been refreshed",
            "data": {"access_token": new_access_token, "token_type": 'bearer'}}


@rt.post("/login", summary="Sign on")
def login_user(response: Response, user = Depends(verify_auth_user), refresh_conn: RefreshTokensRepositories = Depends(get_refresh_tokens_repositories)):
    jti = str(uuid.uuid4())
    access_payload = {
        "sub": str(user.id),
        "is_verified": user.is_verified}
    refresh_payload = {
        "sub": str(user.id),
        "jti": jti}

    refresh_conn.delete_token_data_by_user_id(user_id=user.id)
    access_token = create_access_token(payload=access_payload)
    refresh_token = create_refresh_token(payload=refresh_payload)



    refresh_conn.add_refresh_token(user_id=user.id, token_hash=hash_token(refresh_token),
                                   expires_at=(datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)), jti=jti)
    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        httponly=True,
                        samesite="strict",
                        secure=False,
                        max_age=60*60*24*30,
                        path="/auth/refresh"
                        )
    return {"message": f"User {user.fullname} is logged in",
            "data": {"access_token": access_token, "token_type": "Bearer"}}
