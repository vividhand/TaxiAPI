import os
from email.message import EmailMessage
from dotenv import load_dotenv
import aiosmtplib
from pathlib import Path
import random
from repositories.verification import OrderVerifyRepositories
import secrets
from repositories.driver import DriverRepositories
from repositories.verification import EmailVerifyRepositories
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "Core" / ".env")


def get_driver_id(email: str):
    conn = DriverRepositories()
    driver_data = conn.select_driver_data_by_email(driver_email=email)
    if driver_data[0]:
        return driver_data[1][0]
    return driver_data[1]
async def send_email_to_driver(email: str, user_fullname: str, location: str):
    order_code= random.randint(100000, 999999)
    token = secrets.token_urlsafe(32)
    message = EmailMessage()
    message["From"] = "Taxi API <noreply@taxiapi.local>"
    message["To"] = email

    message.set_content(f"New order with passenger: {user_fullname}. Location: {location}."
                        f"Confirm your order on the website! Order code: {order_code}. Order token: {token}. Or click on this link:"
                        f"http://127.0.0.1:200/verify_order?order_token={token}&code={order_code}"
                        f"")
    driver_id = get_driver_id(email=email)
    if driver_id == "Not found":
        return False


    conn_to_verify_order = OrderVerifyRepositories()
    conn_to_verify_order.add_code(driver_id=driver_id, code=order_code, token=token)

    result = await aiosmtplib.send(
        message,
        hostname="sandbox.smtp.mailtrap.io",
        port=2525,
        username=os.getenv("SANDBOX_USERNAME"),
        password=os.getenv("SANDBOX_PASSWORD"),
        start_tls=True,
    )
    return result

async def send_email_to_verify(email: str, subject: str, token: str):
    verify_code = random.randint(100000, 999999)
    message = EmailMessage()
    message["From"] = "Taxi API <noreply@taxiapi.local>"
    message["To"] = email
    message["Subject"] = subject

    message.set_content(f"Your verification code: {verify_code}")
    conn = EmailVerifyRepositories()
    conn.add_code(token=token, code=verify_code, email=email)
    result = await aiosmtplib.send(
        message,
        hostname="sandbox.smtp.mailtrap.io",
        port=2525,
        username=os.getenv("SANDBOX_USERNAME"),
        password=os.getenv("SANDBOX_PASSWORD"),
        start_tls=True,
    )
    return result
