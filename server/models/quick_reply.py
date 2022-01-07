from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class QuickReply(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    access_token: str
    intent: Optional[str] = None
    texts: Optional[list] = []
    labels: Optional[list] = []
    reply: Optional[list] = []

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "hello",
                "access token": "access token long live",
                "intent": "hello world",
                "texts": ["what name", "what product"],
                "labels": ["name", "product"],
                "reply": ["hello ja", "swadee ja"],
            }
        }


class TokenUser(QuickReply):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateQuickReply(BaseModel):
    name: str
    access_token: str
    intent: Optional[str] = None
    texts: Optional[list] = []
    labels: Optional[list] = []
    reply: Optional[list] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "update hello",
                "access token": "update access token long live",
                "intent": "update hello world",
                "texts": ["what name", "what product"],
                "labels": ["name", "product"],
                "reply": ["hello ja", "swadee ja"],
            }
        }
