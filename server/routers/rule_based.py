from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter
from db import db, generate_token
from fastapi.encoders import jsonable_encoder

router = APIRouter()
collection = 'rule_based'


class RuleBased(BaseModel):
    name: str
    access_token: str
    status_flex: Optional[bool] = False
    content: Optional[str] = None
    keyword: Optional[list] = []
    answer: Optional[list] = []


class TokenUser(RuleBased):
    id: Optional[str] = None
    uid: Optional[str] = None


def get_rule_based_user(access_token):
    users = db.find(collection=collection, query={'access_token': access_token})


@router.post('/create')
async def create_rule_based():
    pass


@router.get('/')
async def get_rule_based():
    pass


@router.put('/query/update')
async def update_rule_based():
    pass


@router.delete('/query/delete')
async def delete_rule_based():
    pass
