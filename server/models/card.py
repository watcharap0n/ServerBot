from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class Card(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    access_token: str
    content: Optional[str] = None
    message: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "flex hello",
                "access_token": "access token long live",
                "content": "input your flex message json",
                "message": "description flex message",
            }
        }


class TokenUser(Card):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateCard(BaseModel):
    name: str
    access_token: str
    content: Optional[str] = None
    message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "update flex hello",
                "access_token": "access token long live",
                "content": "update input your flex message json",
                "message": "update description flex message",
            }
        }
