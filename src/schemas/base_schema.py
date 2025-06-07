from pydantic import BaseModel
from typing import TypeVar

class BaseSchema(BaseModel):
    model_config = {"from_attributes": True}

class CreateSchema(BaseSchema):
    pass

class UpdateSchema(BaseSchema):
    pass

BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseSchema)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateSchema)