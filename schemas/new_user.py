from pydantic import BaseModel, Field

#Schema for new user
class UserSchema(BaseModel):
    fullname: str = Field(min_length=4, max_length=64)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class UserResponseSchema(UserSchema):
    id: int
    is_admin: bool = False
    is_verified: bool = False

class UserSchemaResponse(BaseModel):
    fullname: str = Field(min_length=4, max_length=64)
    email: str = Field(min_length=4, max_length=64)
