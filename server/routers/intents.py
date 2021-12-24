from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from db import db, generate_token
from routers.secure import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = 'intents'


class Intent(BaseModel):
    name: str
    access_token: str
    status_flex: Optional[bool] = False
    content: Optional[str] = None
    question: Optional[list] = []
    answer: Optional[list] = []


class TokenUser(Intent):
    id: Optional[str] = None
    uid: Optional[str] = None


def get_intent(access_token):
    user = db.find_one(collection=collection,
                       query={'access_token': access_token})
    if not user:
        return False
    user = TokenUser(**user)
    return user


async def verify_name_intent(intent: Intent):
    user = get_intent(intent.access_token)
    if user:
        if user.name == intent.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Invalid value key name duplicate')
    return intent


@router.post('/create', response_model=TokenUser)
async def create_intent(intent: Intent = Depends(verify_name_intent),
                        current_user: User = Depends(get_current_active)):
    Id = generate_token(engine=ObjectId())
    item_model = jsonable_encoder(intent)
    item_model['id'] = Id
    item_model['uid'] = current_user.data.uid
    db.insert_one(collection=collection, data=item_model)
    store_model = TokenUser(**item_model)
    return store_model


@router.get('/get')
async def get_intents(access_token: Optional[str] = None,
                      current_user: User = Depends(get_current_active)):
    user = db.find(collection=collection, query={'access_token': access_token})
    user = list(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not found intents')
    return user


@router.put('/query/update/{id}')
async def update_intent(id: str, intent: Intent,
                        current_user: User = Depends(get_current_active)):
    data = jsonable_encoder(intent)
    query = {'id': id}
    values = {'$set': data}
    db.update_one(collection=collection, query=query, values=values)
    return {'detail': f'Update success {id}'}


@router.delete('/query/delete/{id}')
async def delete_intent(id: str,
                        current_user: User = Depends(get_current_active)):
    try:
        db.delete_one(collection=collection, query={'id': id})
        return {'detail': f'Delete success {id}'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid data message')
