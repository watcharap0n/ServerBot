from db import db
from typing import List, Optional
from oauth2 import get_current_active, User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.image_map import ImageMap, TokenUser
from modules.item_static import item_user

router = APIRouter()

collection = 'images_map'


@router.get('/items', response_model=List[TokenUser])
async def images_map(access_token: str):
    items = await db.find(collection=collection,
                          query={'access_token': access_token})
    return items


async def check_name_image(image: ImageMap):
    item = await db.find_one(collection=collection,
                             query={'access_token': image.access_token, 'name': image.name})
    if item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid duplicate name')
    return image


@router.get('/item/{id}', response_model=TokenUser)
async def image_map(access_token: str, id: str):
    item = await db.find_one(collection=collection,
                             query={'access_token': access_token, '_id': id})
    return item


@router.post('/item', response_model=TokenUser)
async def add_image_map(image: ImageMap, current_user: User = Depends(get_current_active)):
    item_model = jsonable_encoder(image)
    await db.insert_one(collection=collection, data=item_model)
    item_model = item_user(item_model, current_user)
    item_store = TokenUser(**item_model)
    return item_store
