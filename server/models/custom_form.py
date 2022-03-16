from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class CustomForm(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: Optional[str] = None
    id_form: Optional[str] = None
    endpoint: Optional[str]
    models: Optional[list] = []
    access_token: str

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "form name",
                "id_form": "1",
                "endpoint": "url",
                "models": ['model1', 'model2'],
                "access_token": "token long live"

            }
        }


class TokenUser(CustomForm):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateForm(BaseModel):
    name: Optional[str] = None
    id_form: Optional[str] = None
    endpoint: Optional[str] = None
    models: Optional[list] = []
    access_token: str

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "update name",
                "id_form": "1",
                "endpoint": "url",
                "models": ['model1', 'model2'],
                "access_token": "token long live"
            }

        }
