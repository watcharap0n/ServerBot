from db import PyObjectId
from typing import Optional, Any
from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl
from models.notification import DefaultCard


class MessageFactory(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    display_name: Optional[str] = None
    user_id: Optional[str] = None
    access_token: Optional[str] = None
    img: Optional[HttpUrl] = None
    status: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "display_name": "kane",
                "user_id": "U12345",
                "access_token": "access token long live",
                "img": "https://imageexample.com",
                "status": "application"
            }
        }


class PushMessage(BaseModel):
    user_id: str
    access_token: str
    message: Optional[str] = 'None'

    class Config:
        schema_extra = {
            "example": {
                "user_id": "U12345",
                "access_token": "access token long live",
                "message": "hello world"
            }
        }


class PushFlex(BaseModel):
    user_id: str
    access_token: str
    id_card: Any

    class Config:
        schema_extra = {
            "example": {
                "user_id": "U12345",
                "access_token": "access token long live",
                "id_card": "your id card"
            }
        }


class PushFlexDefault(BaseModel):
    user_id: str
    access_token: str
    content: dict
    config_default_card: Optional[DefaultCard] = {
        "header": "header card",
        "image": False,
        "path_image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "footer": False,
        "body_key": ['name', 'company'],
        "body_value": ['watcharapon', 'mango consultant'],
        "name_btn": "URL",
        "url_btn": "https://mangoserverbot.herokuapp.com"
    }

    class Config:
        schema_extra = {
            "example": {
                "user_id": "U12345",
                "access_token": "access token long live",
            }
        }


class PushImage(BaseModel):
    user_id: str
    access_token: str
    image_original: str
    image_preview: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "U12345",
                "access_token": "access token long live",
                "image_original": "https://exampleOriginal.com",
                "image_preview": "https://examplePreview.com"
            }
        }


class PushSticker(BaseModel):
    user_id: str
    access_token: str
    sticker_id: str
    package_id: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "U12345",
                "access_token": "access token long live",
                "sticker_id": "001",
                "package_id": "112"
            }
        }
