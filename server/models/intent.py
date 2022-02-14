from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class Intent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    access_token: str
    ready: Optional[bool] = True
    status_flex: Optional[bool] = False
    card: Optional[str] = None
    question: Optional[list] = []
    answer: Optional[list] = []

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "hello world",
                "access_token": "access token long live",
                "ready": True,
                "status_flex": False,
                "card": "id card flex message",
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
    status_flex: Optional[bool] = False
    card: Optional[str] = None
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
                "status_flex": False,
                "card": "update content flex message",
                "question": ["hello", "update"],
                "answer": ["hello there", "update"],
            }
        }
