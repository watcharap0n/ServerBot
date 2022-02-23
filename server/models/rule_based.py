from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class RuleBased(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    access_token: str
    postback: Optional[bool] = False
    status_flex: Optional[bool] = False
    ready: Optional[bool] = True
    card: Optional[str] = None
    keyword: Optional[str] = None
    answer: Optional[list] = []

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "rule based",
                "access_token": "access token long live",
                "postback": False,
                "status_flex": False,
                "ready": True,
                "card": "id card query collection card",
                "keyword": 'erp',
                "answer": ["answer bot"],
            }
        }


class TokenUser(RuleBased):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

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
    status_flex: Optional[bool] = False
    ready: Optional[bool] = True
    card: Optional[str] = None
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
                "status_flex": False,
                "ready": True,
                "card": "update id card query collection card",
                "keyword": 'erp',
                "answer": ["answer bot"],
            }
        }
