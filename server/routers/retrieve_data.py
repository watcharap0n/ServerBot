from db import db
from typing import Optional, List
from starlette.responses import JSONResponse
from models.retrieve_data import TokenUser, Retrieve, UpdateRetrieve, Transaction
from modules.item_static import item_user
from oauth2 import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = 'retrieve'


@router.get('/')
async def get_retrieve_data(
        access_token: str,
):
    items = await db.find(collection=collection, query={"access_token": access_token})
    items = list(items)
    return items


@router.post("/create", response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def create_retrieve(
        payload: Retrieve,
        current_user: User = Depends(get_current_active),
):
    item_model = jsonable_encoder(payload)
    item_model = item_user(data=item_model, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenUser(**item_model)
    return item_store


@router.put("/query/update/{id}", response_model=UpdateRetrieve)
async def update_query_intent(
        id: str,
        payload: UpdateRetrieve,
):
    value = jsonable_encoder(payload)
    query = {"_id": id}
    values = {"$set": value}

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Retrieved not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_query_intent(id: str):
    if (await db.delete_one(collection=collection, query={"_id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Retrieved not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
