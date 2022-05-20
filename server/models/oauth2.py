from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl
from db import PyObjectId


class Permission(BaseModel):
    uid: str
    username: str
    role: Optional[str] = None
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    img_path: Optional[str] = None
    date: datetime
    time: datetime
    phone_number: Optional[str] = None
    disabled: Optional[bool] = None
    _data: Optional[dict] = None


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    data: Optional[Permission] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {"data": {}}


class UpdateSettingsProfile(BaseModel):
    display_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    photo_url: Optional[HttpUrl] = None
    password: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "display_name": "kane",
                "email": "exmalple@gmail.com",
                "phone_number": "0941499661",
                "photo_url": "https://examples/upload/picture",
                "password": "secret"
            }
        }
