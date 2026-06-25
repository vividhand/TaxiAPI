from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)

class AuthJWTSchema(BaseModel):
    private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expr_time: int = 15

jwt_schem = AuthJWTSchema()