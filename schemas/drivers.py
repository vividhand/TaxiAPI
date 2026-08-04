from pydantic import BaseModel, Field

#Schema for new driver
class DriverSchema(BaseModel):
    fullname: str = Field(min_length=4, max_length=64)
    email: str = Field(min_length=1)


