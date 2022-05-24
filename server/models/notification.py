from datetime import datetime
from db import PyObjectId
from bson import ObjectId
from typing import Optional, Any
from pydantic import BaseModel, Field, HttpUrl


class DefaultCard(BaseModel):
    header: Optional[str] = None
    image: Optional[bool] = False
    path_image: Optional[HttpUrl] = None
    footer: Optional[bool] = False
    body_key: Optional[list] = ['input your key flex msg']
    body_value: Optional[list] = ['input your value flex msg'],
    name_btn: Optional[str] = 'URL',
    url_btn: Optional[HttpUrl] = 'https://linecorp.com'


class Post(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    access_token: str
    flex_status: Optional[bool] = False
    id_card: Optional[str] = None
    content: Optional[dict] = None
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
    message: Optional[str] = 'None'

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "platform user_id",
                "access_token": "access token long live",
                "flex_status": False,
                "id_card": None,
                "content": {'key1': 'value1', 'key2': 'value2'},
                "message": "notification!"
            }
        }


class TokenUser(Post):
    uid: Optional[str] = None
    date: Optional[datetime] = None
    time: Optional[datetime] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }
