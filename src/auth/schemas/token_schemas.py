from src.schemas.base_schema import BaseSchema

class TokenInfo(BaseSchema):    
    access_token: str
    token_type: str