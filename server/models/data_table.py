from db import PyObjectId
from uuid import UUID, uuid4
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, constr


class ColumnDataTable(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    access_token: Optional[str] = None
    text: Optional[str] = None
    value: str = Field(default_factory=uuid4)
    align: Optional[str] = None
    sortable: Optional[bool] = None
    filterable: Optional[bool] = None
    groupable: Optional[bool] = None
    divider: Optional[bool] = None
    _class: Optional[bool] = Field(None, alias="class")
    cellClass: Optional[str] = None
    width: Optional[str] = None
    filter: Optional[str] = None
    sort: Optional[int] = None
    items_select: Optional[list] = []
    type_field: Optional[str] = None
    status: Optional[bool] = True
    default_field: Optional[bool] = False

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "text": "Name",
                "value": "name",
                "access_token": "token long live",
                "align": "center",
                "sortable": False,
                "filterable": False,
                "groupable": False,
                "divider": False,
                "class": False,
                "cellClass": "",
                "width": 200,
                "filter": "",
                "sort": 10,
                "items_select": ['name'],
                "type_field": "default",
                "status": True,
                "default_field": False
            }
        }


class TokenUser(ColumnDataTable):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateDataTable(BaseModel):
    access_token: Optional[str] = None
    text: Optional[str] = None
    value: Optional[str] = None
    align: Optional[str] = None
    sortable: Optional[bool] = None
    filterable: Optional[bool] = None
    groupable: Optional[bool] = None
    divider: Optional[bool] = None
    _class: Optional[bool] = Field(None, alias="class")
    cellClass: Optional[str] = None
    width: Optional[int] = None
    filter: Optional[str] = None
    sort: Optional[int] = None
    items_select: Optional[list] = None
    type_field: Optional[str] = None
    status: Optional[bool] = True
    default_field: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "text": "First Name",
                "value": "fname",
                "align": "center",
                "sortable": False,
                "filterable": False,
                "groupable": False,
                "divider": False,
                "class": False,
                "cellClass": "",
                "width": 200,
                "filter": "",
                "sort": 10,
                "items_select": ['name'],
                "type_field": "default",
                "status": True,
                "default_field": False
            }
        }
