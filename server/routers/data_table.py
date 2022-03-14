from typing import Optional
from db import db
from typing import List
from oauth2 import get_current_active, User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from modules.item_static import item_user
from models.data_table import ColumnDataTable, TokenUser, UpdateDataTable

router = APIRouter()

collection = 'data_table'


@router.get('/find', response_model=List[TokenUser])
async def get_data_table(
        access_token: str,
        status: Optional[bool] = False,
        current_user: User = Depends(get_current_active)
):
    if status:
        data = await db.find(collection=collection, query={'access_token': access_token, 'status': status})
        data = list(data)
        return data

    data = await db.find(collection=collection, query={'access_token': access_token})
    data = list(data)
    return data


@router.post('/create', response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def add_a_column(payload: ColumnDataTable,
                       current_user: User = Depends(get_current_active)):
    item_model = jsonable_encoder(payload)
    item_model = item_user(item_model, current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenUser(**item_model)
    return item_store


@router.put('/query/update/{id}', response_model=UpdateDataTable)
async def update_a_column(id: str, payload: UpdateDataTable,
                          current_user: User = Depends(get_current_active)):
    item_model = jsonable_encoder(payload)
    value = {'$set': item_model}
    query = {'_id': id}
    if (await db.update_one(collection=collection, query=query, values=value)) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'column not found or update already exist')
    return payload


@router.delete('/query/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_column(id: str, current_user: User = Depends(get_current_active)):
    if (await db.delete_one(collection=collection, query={'_id': id})) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'column not found {id}')
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
