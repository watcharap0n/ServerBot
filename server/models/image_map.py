from db import PyObjectId
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field


class Map(BaseModel):
    area: Optional[dict] = None
    data: Optional[str] = None
    type: Optional[str] = None


class ImageMap(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    access_token: str
    width: int
    height: int
    description: Optional[str] = None
    map: Optional[List[Map]] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "hello mapping",
                "access_token": "token long live",
                "width": 240,
                "height": 480,
                "map": [
                    {
                        "area": {'x': 0, 'y': 0, 'w': 0, 'h': 0},
                        "data": "send data",
                        "type": 'message'
                    }
                ],
                "description": "description mapping",
            }
        }


class TokenUser(ImageMap):
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
    width: int
    height: int
    description: Optional[str] = None
    map: Optional[List[Map]] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "update mapping",
                "access_token": "update token long live",
                "width": 250,
                "height": 500,
                "map": [
                    {
                        "area": {'x': 0, 'y': 0, 'w': 0, 'h': 0},
                        "data": "update send data",
                        "type": 'update message'
                    }
                ],
                "description": "update description mapping",
            }
        }
