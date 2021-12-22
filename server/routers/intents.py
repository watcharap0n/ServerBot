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
    flex_message: Optional[str] = None
    question: Optional[list] = []
    answer: Optional[list] = []


class TokenUser(Intent):
    uid: Optional[str] = None


def get_intent(access_token):
    user = db.find_one(collection=collection,
                       query={'access_token': access_token})
    user = TokenUser(**user)
    return user


async def verify_name_intent(intent: Intent):
    user = db.find(collection=collection, query={'uid': intent.name})
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid value key name duplicate')
    user = TokenUser(**user)
    return user


@router.post('/create', response_model=TokenUser)
async def create_intent(item_model: dict = Depends(verify_name_intent),
                        current_user: User = get_current_active):
    Id = generate_token(engine=ObjectId())
    item_model['id'] = Id
    item_model['uid'] = current_user.uid
    db.insert_one(collection=collection, data=item_model)
    store_model = TokenUser(**item_model)
    return store_model


@router.get('/get', response_model=TokenUser)
async def get_intents(access_token: Optional[str] = None):
    user = get_intent(access_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not found intents')
    return user



