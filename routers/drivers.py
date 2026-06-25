from fastapi import APIRouter, HTTPException, Depends, status
from repositories.verification import OrderVerifyRepositories
from repositories.order import OrderRepositories
from services.get_user_role import get_user_role

rt = APIRouter(tags=["Drivers"])


@rt.post("/verify_order")
def verify_order(order_token: str, code: int, role: dict = Depends(get_user_role)):
    if role["role"] != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a driver")
    conn = OrderVerifyRepositories()
    order_data = conn.select_code(order_token=order_token)
    if order_data[0]:
        if order_data[1][2] == code:

            return {"status": 200,
                    "message": "Order has been verified. Go to the location indicated in the message."}
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid verification code")
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid order token")