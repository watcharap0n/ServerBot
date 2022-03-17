from typing import Optional, Any
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class Intent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    access_token: str
    ready: Optional[bool] = True
    type_reply: Optional[str] = None
    card: Optional[Any] = None
    image: Optional[Any] = None
    question: Optional[list] = []
    answer: Optional[list] = []

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "hello world",
                "access_token": "access token long live",
                "ready": True,
                "type_reply": "Text",
                "card": {
                    "_id": "1234",
                    "name": "name flex message",
                    "content": "content flex message"
                },
                "image": {
                    "_id": "1234",
                },
                "question": ["hello"],
                "answer": ["hello there"],
            }
        }


class TokenUser(Intent):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateIntent(BaseModel):
    name: str
    access_token: str
    ready: Optional[bool] = True
    type_reply: Optional[str] = None
    card: Optional[Any] = None
    image: Optional[Any] = None
    question: Optional[list] = []
    answer: Optional[list] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "update hello world",
                "access_token": "update access token long live",
                "ready": True,
                "type_reply": "Text",
                "card": {
                    "_id": "1234",
                    "name": "name flex message",
                    "content": "content flex message"
                },
                "image": {
                    "_id": "1234",
                },
                "question": ["hello", "update"],
                "answer": ["hello there", "update"],
            }
        }
