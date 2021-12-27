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
    users = db.find(collection=collection, query={'uid': uid})
    users = list(users)
    users = UserList.parse_obj(users)
    return users


async def check_flex_user(item: FlexModel,
                          current_user: User = Depends(get_current_active)):
    Id = generate_token(engine=ObjectId())
    item_model = jsonable_encoder(item)
    item_model['uid'] = current_user.data.uid
    item_model['id'] = Id
    user = TokenUser(**item_model)
    users = get_flex_user(user.uid)
    users = jsonable_encoder(users)
    for i in users:
        if i['name'] == item.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Invalid name duplicate')
    return user


@router.get('/', response_model=UserList)
async def get_flex(current_user: User = Depends(get_current_active)):
    items = get_flex_user(current_user.data.uid)
    if not items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not found flex message')
    return items


@router.post('/create', response_model=TokenUser)
async def create_flex(user: TokenUser = Depends(check_flex_user),
                      current_user: User = Depends(get_current_active)):
    item_store = jsonable_encoder(user)
    db.insert_one(collection=collection, data=item_store)
    return item_store


@router.put('/query/update/{id}')
async def update_flex(id: str, flex: FlexModel,
                      current_user: User = Depends(get_current_active)):
    data = jsonable_encoder(flex)
    query = {'id': id}
    values = {'$set': data}
    db.update_one(collection=collection, query=query, values=values)
    return {'detail': f'Update success {id}'}


@router.delete('/query/delete/{id}')
async def delete_flex(id: str,
                      current_user: User = Depends(get_current_active)):
    try:
        db.delete_one(collection=collection, query={'id': id})
        return {'detail': f'Delete success {id}'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid data message')
