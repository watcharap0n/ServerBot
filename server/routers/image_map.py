import json
from typing import Optional, Any
from db import db
from typing import List
from oauth2 import get_current_active, User
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.image_map import ImageMap, TokenUser, Mapping, UpdateImageMap
from modules.item_static import item_user

router = APIRouter()

collection = 'images_map'


async def check_name_image(image: ImageMap):
    item = await db.find_one(collection=collection,
                             query={'access_token': image.access_token, 'name': image.name})
    if item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid duplicate name.')
    return image


def json_loads_encoder(content):
    if content:
        return json.loads(content)
    pass


@router.get('/', response_model=List[TokenUser])
async def images_map(access_token: str):
    items = await db.find(collection=collection,
                          query={'access_token': access_token})
    items = list(items)
    return items


@router.get('/{id}', response_model=TokenUser)
async def image_map(access_token: str, id: str):
    item = await db.find_one(collection=collection,
                             query={'access_token': access_token, '_id': id})
    return item


@router.post('/create', response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def add_image_map(image: ImageMap = Depends(check_name_image),
                        current_user: User = Depends(get_current_active)):
    content = json_loads_encoder(image.content)
    item_model = jsonable_encoder(image)
    item_model['size'] = content.get('size') if content else None
    item_model['areas'] = content.get('areas') if content else None
    item_model_mapping = Mapping(**item_model)
    item_model_mapping = jsonable_encoder(item_model_mapping)
    item_model_mapping = item_user(item_model_mapping, current_user)
    await db.insert_one(collection=collection, data=item_model_mapping)
    item_store = TokenUser(**item_model_mapping)
    return item_store


@router.put('/query/update/{id}', response_model=UpdateImageMap)
async def update_image_map(payload: UpdateImageMap, id: str):
    content = json_loads_encoder(payload.content)
    item_model = jsonable_encoder(payload)
    item_model['size'] = content.get('size') if content else None
    item_model['areas'] = content.get('areas') if content else None
    query = {'_id': id}
    value = {'$set': item_model}
    item_store = UpdateImageMap(**item_model)
    if (await db.update_one(collection=collection, query=query, values=value)) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'id item not found in {id}')
    return item_store


@router.delete('/query/delete/{id}')
async def delete_image_map(id: str):
    if (await db.delete_one(collection=collection, query={'_id': id})) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'id item not found in {id}')
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/json/encoder')
async def api_json_encoder(payload: Optional[Any] = Body(None)):
    return json.dumps(payload)
