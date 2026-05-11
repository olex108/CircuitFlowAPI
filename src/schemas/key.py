from pydantic import BaseModel
from pydantic import EmailStr


class CreateApi(BaseModel):
    email : EmailStr
    password: str


class ApiKeyOut(BaseModel):
    model_config = {"from_attributes": True}

    api_key: str
