# models/key.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class ApiKey(BaseModel):

    __tablename__ = "api_keys"

    email : Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password : Mapped[str] = mapped_column(String(1024), nullable=False)
    hashed_api_key : Mapped[str] = mapped_column(String(1024), primary_key=True)
    is_active : Mapped[bool] = mapped_column(default=False)
