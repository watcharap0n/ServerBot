from bson import ObjectId
from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends
from db import db, generate_token
from routers.secure import User, get_current_active
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


class UserList(BaseModel):
    __root__: List[TokenUser]


def get_rule_based_user(access_token):
    users = db.find(collection=collection,
                    query={'access_token': access_token})
    users = list(users)
    users = UserList.parse_obj(users)
    return users


async def verify_name_rule(item: RuleBased):
    users = get_rule_based_user(item.access_token)
    users = jsonable_encoder(users)
    if users:
        for user in users:
            if user['name'] == item.name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Invalid name duplicate')
    return item


@router.post('/create', response_model=TokenUser)
async def create_rule_based(payload: RuleBased = Depends(verify_name_rule),
                            current_user: User = Depends(get_current_active)):
    Id = generate_token(engine=ObjectId())
    item_model = jsonable_encoder(payload)
    item_model['id'] = Id
    item_model['uid'] = current_user.data.uid
    db.insert_one(collection=collection, data=item_model)
    store_model = TokenUser(**item_model)
    return store_model


@router.get('/', response_model=UserList)
async def get_rule_based(access_token: Optional[str] = None,
                         current_user: User = Depends(get_current_active)):
    users = get_rule_based_user(access_token)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not found intents')
    return users


@router.put('/query/update/{id}')
async def update_rule_based(id: str,
                            payload: RuleBased,
                            current_user: User = Depends(get_current_active)):
    data = jsonable_encoder(payload)
    query = {'id': id}
    values = {'$set': data}
    db.update_one(collection=collection, query=query, values=values)
    return {'detail': f'Update success {id}'}


@router.delete('/query/delete/{id}')
async def delete_rule_based(id: str,
                            current_user: User = Depends(get_current_active)):
    try:
        db.delete_one(collection=collection, query={'id': id})
        return {'detail': f'Delete success {id}'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid data message')
