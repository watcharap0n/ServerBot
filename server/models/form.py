from db import PyObjectId
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field


class FormPage(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    id_form: Optional[str] = None

