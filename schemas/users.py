import datetime
from pydantic import BaseModel, Field, ConfigDict

class NewUserSchema(BaseModel):
    fullname: str = Field(min_length=4, max_length=64)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class UserSchema(BaseModel):
    id: int
    fullname: str
    email: str
    password: str
    registration_date: datetime.datetime
    is_admin: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)