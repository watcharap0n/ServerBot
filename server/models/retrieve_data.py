from db import PyObjectId
from typing import Optional, Any, List
from bson import ObjectId
from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction: Optional[dict] = None


class Retrieve(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    access_token: str
    transaction: Optional[dict] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "access_token": "access token long live",
                "transaction":
                    {
                        'fname': 'watcharapon',
                        'lname': 'weeraborirak',
                        'name': 'kane'
                    }

            }
        }


class TokenUser(Retrieve):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateRetrieve(BaseModel):
    transaction: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "transaction":
                    {
                        'fname': 'watcharapon',
                        'lname': 'weeraborirak',
                        'name': 'kane'
                    }

            }
        }
