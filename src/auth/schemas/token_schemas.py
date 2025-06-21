from src.schemas.base_schema import BaseSchema

class TokenInfo(BaseSchema):    
    access_token: str
    refrash_token: str
    token_type: str

class AccessTokenInfo(BaseSchema):
    access_token: str
    token_type: str

class RefrashTokenInfo(BaseSchema):
    refrash_token: str