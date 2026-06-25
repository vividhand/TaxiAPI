from pydantic import BaseModel, Field
from core.setting import Rate
class ReviewSchema(BaseModel):

    username: str
    driver_name: str
    rate: Rate
    text: str = Field(max_length=500)