from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class LineToken(BaseModel):
    token: PyObjectId = Field(default_factory=PyObjectId, alias="token")
    name: str
    access_token: str
    secret_token: str

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "name callback",
                "access_token": "access token long live",
                "secret_token": "secret token",
            }
        }


class Webhook(LineToken):
    uid: Optional[str] = None
    url: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "url": "https://mangoserverbot.herokuapp.com/callback/token",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateLineToken(BaseModel):
    name: str
    access_token: str
    secret_token: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "update name callback",
                "access_token": "access token long live",
                "secret_token": "secret token",
            }
        }
