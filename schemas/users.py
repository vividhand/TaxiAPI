import datetime
from pydantic import BaseModel, Field, ConfigDict

class NewUserSchema(BaseModel):
    fullname: str = Field(min_length=4, max_length=64)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
