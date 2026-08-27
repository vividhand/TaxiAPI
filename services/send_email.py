import os
from email.message import EmailMessage
from dotenv import load_dotenv
import aiosmtplib
from pathlib import Path
import random
import secrets
from fastapi import HTTPException, status

from repositories import DriverRepositories, EmailVerifyRepositories, OrderVerifyRepositories
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "Core" / ".env")


def get_driver_id(email: str):
    driver_connect = DriverRepositories()
    driver_data = driver_connect.select_driver_data_by_email(driver_email=email)
    return driver_data

async def send_email_to_driver(order_id: int, email: str, user_fullname: str, location: str):
    order_code = random.randint(100000, 999999)
    token = secrets.token_urlsafe(32)
    message = EmailMessage()
    message["From"] = "Taxi API <noreply@taxiapi.local>"
    message["To"] = email

    message.set_content(f"New order with passenger: {user_fullname}. Location: {location}."
                        f"Confirm your order on the website! Order code: {order_code}.\n"
                        f"Order token: {token})")
    driver_id = get_driver_id(email=email).id
    if driver_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")




    conn_to_verify_order = OrderVerifyRepositories()
    conn_to_verify_order.add_code(order_id=order_id, driver_id=driver_id, code=order_code, token=token)

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
    response = conn.add_code(token=token, code=verify_code, email=email)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

    result = await aiosmtplib.send(
        message,
        hostname="sandbox.smtp.mailtrap.io",
        port=2525,
        username=os.getenv("SANDBOX_USERNAME"),
        password=os.getenv("SANDBOX_PASSWORD"),
        start_tls=True,
    )
    return result
