from pydantic import BaseModel

class NewOrderSchema(BaseModel):

    driver_email: str
    location: str