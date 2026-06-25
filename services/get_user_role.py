from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from auth.utils import jwt_decode
from repositories.user import UserRepositories
from repositories.driver import DriverRepositories

http_bearer = HTTPBearer()

def get_user_role(cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> list:
    jwt_encoded_token = cred.credentials
    try:
        decoded_token = jwt_decode(jwt_token=jwt_encoded_token)
        user_email = decoded_token[2]
        conn_to_user = UserRepositories()
        user_data = conn_to_user.select_user_by_email(email=user_email)
        if user_data[0]:
            user_id = user_data[1][0]
            if user_data[1][4] == True:
                return [True, {"user_id": user_id, "role": "admin"}]
            conn_to_driver = DriverRepositories()
            driver_data = conn_to_driver.select_driver_data_by_id(driver_id=user_id)
            if driver_data[0]:
                return [True, {"user_id": user_id, "role": "driver"}]
            return [True, {"user_id": user_id, "role": "user"}]
    except Exception as e:
        return [False, str(e)]

