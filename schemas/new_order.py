from pydantic import BaseModel

class NewOrderSchema(BaseModel):

    driver_fullname: str
    location: str