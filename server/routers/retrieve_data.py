from bson import ObjectId
from db import db, generate_token
from typing import Optional, Any
from starlette.responses import JSONResponse
from modules.item_static import item_user
from oauth2 import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status, Body

router = APIRouter()

collection = 'retrieve'


@router.get('/find')
async def get_retrieve_data(access_token: str):
    items = await db.find(collection=collection,
                          query={"access_token": access_token},
                          select_field={"_id": 0})
    items = list(items)
    return items


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_retrieve(
        access_token: str,
        payload: Optional[Any] = Body(None),
        current_user: User = Depends(get_current_active),
):
    ids = generate_token(engine=ObjectId())
    payload['id'] = ids
    payload['access_token'] = access_token
    item_model = item_user(data=payload, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    del item_model["_id"]
    return item_model


@router.put("/query/update/{id}")
async def update_query_intent(
        id: str,
        payload: Optional[Any] = Body(None),
):
    query = {"id": id}
    values = {"$set": payload}

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Retrieved not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_query_intent(id: str):
    if (await db.delete_one(collection=collection, query={"id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Retrieved not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
