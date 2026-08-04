from pydantic import BaseModel

class RefreshRequestSchemas(BaseModel):
    refresh_token: str