from typing import Optional, List
from pydantic import BaseModel
from modules.item_static import item_user
from db import db, generate_token
from routers.secure import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = 'intents'


class Intent(BaseModel):
    name: str
    access_token: str
    ready: Optional[bool] = True
    status_flex: Optional[bool] = False
    content: Optional[str] = None
    question: Optional[list] = []
    answer: Optional[list] = []


class TokenUser(Intent):
    id: Optional[str] = None
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None


class UserList(BaseModel):
    __root__: List[TokenUser]


def get_intents_user(access_token):
    users = db.find(collection=collection,
                    query={'access_token': access_token})
    users = list(users)
    users = UserList.parse_obj(users)
    return users


async def verify_name_intents(intent: Intent):
    users = get_intents_user(intent.access_token)
    users = jsonable_encoder(users)
    if users:
        for user in users:
            if user['name'] == intent.name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Invalid name duplicate')
    return intent


@router.post('/create', response_model=TokenUser)
async def create_intent(intent: Intent = Depends(verify_name_intents),
                        current_user: User = Depends(get_current_active)):
    item_model = jsonable_encoder(intent)
    item_model = item_user(data=item_model, current_user=current_user)
    db.insert_one(collection=collection, data=item_model)
    store_model = TokenUser(**item_model)
    return store_model


@router.get('/', response_model=UserList)
async def get_intents(access_token: Optional[str] = None,
                      current_user: User = Depends(get_current_active)):
    users = get_intents_user(access_token)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not found intents')
    return users


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
