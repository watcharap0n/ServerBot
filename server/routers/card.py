import json
from typing import Optional, List
from pydantic import BaseModel, parse_obj_as
from bson import ObjectId
from db import db, generate_token
from fastapi import APIRouter, Depends, status, HTTPException
from routers.secure import User, get_current_active
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = 'flex_message'


class FlexModel(BaseModel):
    name: str
    content: Optional[str] = None
    message: Optional[str] = None


class TokenUser(FlexModel):
    id: Optional[str] = None
    uid: Optional[str] = None


class UserList(BaseModel):
    __root__: List[TokenUser]


def get_flex_user(uid):
    user = db.find(collection=collection, query={'uid': uid})
    user = list(user)
    users = parse_obj_as(List[TokenUser], user)
    return users


async def check_flex_user(item: FlexModel,
                          current_user: User = Depends(get_current_active)):
    Id = generate_token(engine=ObjectId())
    item_model = jsonable_encoder(item)
    item_model['uid'] = current_user.data.uid
    item_model['id'] = Id
    user = TokenUser(**item_model)
    users = get_flex_user(user.uid)
    for i in users:
        if i.name == item.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Invalid name duplicate')
    return user


@router.get('/')
async def get_flex(uid: Optional[str] = None):
    user = db.find(collection=collection, query={'uid': uid})
    user = list(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not found flex message')
    return user


@router.post('/create', response_model=TokenUser)
async def create_flex(user: TokenUser = Depends(check_flex_user)):
    item_store = jsonable_encoder(user)
    db.insert_one(collection=collection, data=item_store)
    return item_store


@router.put('/query/update/{id}')
async def update_flex(id: str, flex: FlexModel):
    data = jsonable_encoder(flex)
    query = {'id': id}
    values = {'$set': data}
    db.update_one(collection=collection, query=query, values=values)
    return {'detail': f'Update success {id}'}


@router.delete('/query/delete/{id}')
async def delete_flex(id: str):
    try:
        db.delete_one(collection=collection, query={'id': id})
        return {'detail': f'Delete success {id}'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid data message')
