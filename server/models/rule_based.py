from datetime import datetime
from typing import Optional, Any
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class RuleBased(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    access_token: str
    postback: Optional[bool] = False
    type_reply: Optional[str] = None
    ready: Optional[bool] = True
    card: Optional[Any] = None
    image: Optional[Any] = None
    keyword: Optional[str] = None
    answer: Optional[list] = []

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "rule based",
                "access_token": "access token long live",
                "postback": False,
                "type_reply": "Text",
                "ready": True,
                "card": {
                    "_id": "1234",
                    "name": "name flex message",
                    "content": "content flex message"
                },
                "image": {"_id": "1234"},
                "keyword": 'erp',
                "answer": ["answer bot"],
            }
        }


class TokenUser(RuleBased):
    uid: Optional[str] = None
    date: Optional[datetime] = None
    time: Optional[datetime] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateRuleBased(BaseModel):
    name: str
    access_token: str
    postback: Optional[bool] = False
    type_reply: Optional[str] = None
    ready: Optional[bool] = True
    card: Optional[Any] = None
    image: Optional[Any] = None
    keyword: Optional[str] = None
    answer: Optional[list] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "update rule based",
                "access_token": "access token long live",
                "postback": False,
                "type_reply": "Text",
                "ready": True,
                "card": {
                    "_id": "1234",
                    "name": "name flex message",
                    "content": "content flex message"
                },
                "image": {"_id": "1234"},
                "keyword": 'erp',
                "answer": ["answer bot"],
            }
        }
