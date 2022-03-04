from db import db
from typing import List
from oauth2 import get_current_active, User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from models.image_map import ImageMap, TokenUser, UpdateImageMap
from modules.item_static import item_user

router = APIRouter()

collection = 'images_map'


async def check_access_token(image: ImageMap):
    try:
        line_bot_api = LineBotApi(image.access_token)
        line_bot_api.get_bot_info()
        return image
    except LineBotApiError as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)


async def check_name_image(image: ImageMap = Depends(check_access_token)):
    item = await db.find_one(collection=collection,
                             query={'access_token': image.access_token, 'name': image.name})
    if item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid duplicate name.')
    return image


@router.get('/', response_model=List[TokenUser])
async def images_map(access_token: str):
    items = await db.find(collection=collection,
                          query={'access_token': access_token})
    return items


@router.get('/{id}', response_model=TokenUser)
async def image_map(access_token: str, id: str):
    item = await db.find_one(collection=collection,
                             query={'access_token': access_token, '_id': id})
    return item


@router.post('/create', response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def add_image_map(image: ImageMap = Depends(check_name_image),
                        current_user: User = Depends(get_current_active)):
    item_model = jsonable_encoder(image)
    await db.insert_one(collection=collection, data=item_model)
    item_model = item_user(item_model, current_user)
    item_store = TokenUser(**item_model)
    return item_store


@router.put('/query/update/{id}', response_model=UpdateImageMap)
async def update_image_map(payload: UpdateImageMap, id: str):
    item_model = jsonable_encoder(payload)
    query = {'_id': id}
    value = {'$set': item_model}
    if (await db.update_one(collection=collection, query=query, values=value)) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'id item not found in {id}')
    return payload


@router.delete('/query/delete/{id}')
async def delete_image_map(id: str):
    if (await db.delete_one(collection=collection, query={'_id': id})) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'id item not found in {id}')
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
