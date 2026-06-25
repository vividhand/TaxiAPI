import jwt
from schemas.auth_jwt import jwt_schem
import bcrypt
from datetime import datetime, UTC, timedelta
from password_validator import PasswordValidator
from email_validator import validate_email, EmailNotValidError
import hashlib
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30
ACCESS_TOKEN_TYPE = "access_token"
REFRESH_TOKEN_TYPE = "refresh_token"


def jwt_encode(expire_timedelta: datetime, payload: dict, private_key: str = jwt_schem.private_key.read_text(), algorithm_: str = jwt_schem.algorithm):
    to_encode = payload.copy()
    now = datetime.now(UTC)


    to_encode.update(exp=expire_timedelta, iat=now)
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm_)
    return encoded


def jwt_decode(jwt_token: bytes, public_key: str = jwt_schem.public_key.read_text(),
               algorithm_: str = jwt_schem.algorithm):
    decoded = jwt.decode(jwt_token, key=public_key, algorithms=[algorithm_])
    return decoded

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    hashed = bcrypt.hashpw(password_bytes, salt)
    hashed_decode = hashed.decode()
    return hashed_decode
def hash_token(token: str) -> str:
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    return hashed_token

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password.encode())

def verify_token(token: str, hashed_token: str) -> bool:
    if hashlib.sha256(token.encode()).hexdigest() == hashed_token:
        return True
    return False


def email_validate(email, chek_dns: bool = False):
    try:
        validate_email(email, check_deliverability=chek_dns)
        return True
    except EmailNotValidError:
        return False

shema = PasswordValidator()\
.min(8).max(100)\
.has().uppercase()\
.has().lowercase()\
.has().digits()

def password_validate(password: str):
     return shema.validate(password)

def create_token(payload: dict, type: str) -> str:
    jwt_payload = {"type": type}
    jwt_payload.update(payload)
    if type == ACCESS_TOKEN_TYPE:
        expire = datetime.now(UTC) + timedelta(minutes=60)
    elif type == REFRESH_TOKEN_TYPE:
        expire = datetime.now(UTC) + timedelta(days=7)
    return jwt_encode(jwt_payload, expire_timedelta= expire)

def create_access_token(payload: dict):
    access_token = create_access_token(type = ACCESS_TOKEN_TYPE, payload=payload)
    return access_token

def create_refresh_token(payload: dict):
    refresh_token = create_access_token(type=REFRESH_TOKEN_TYPE, payload=payload)
    return refresh_token



