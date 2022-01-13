from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class Permission(BaseModel):
    uid: str
    username: str
    role: Optional[str] = None
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    img_path: Optional[str] = None
    date: str
    time: str
    disabled: Optional[bool] = None
    _data: Optional[dict] = None


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    data: Optional[Permission] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {"data": {}}
