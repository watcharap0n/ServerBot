from db import db
from typing import Optional, List
from starlette.responses import JSONResponse
from models.card import Card, TokenUser, UpdateCard
from modules.item_static import item_user
from oauth2 import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = "card"


@router.get("/", response_model=List[TokenUser])
async def get_card(
        access_token: Optional[str] = None, current_user: User = Depends(get_current_active)
):
    items = await db.find(collection=collection, query={"access_token": access_token})
    items = list(items)
    return items


async def check_duplication_name_card(card: Card):
    items = await db.find(collection=collection, query={"access_token": card.access_token})
    items = list(items)
    for item in items:
        if item['name'] == card.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='card name is duplicate')
    return card


@router.post("/create", response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def create_card(card: Card = Depends(check_duplication_name_card),
                      current_user: User = Depends(get_current_active)):
    items_model = jsonable_encoder(card)
    items_model = item_user(data=items_model, current_user=current_user)
    await db.insert_one(collection=collection, data=items_model)
    item_store = TokenUser(**items_model)
    return item_store


@router.put("/query/update/{id}", response_model=UpdateCard)
async def update_query_card(
        id: str, payload: UpdateCard, current_user: User = Depends(get_current_active)
):
    data = jsonable_encoder(payload)
    query = {"_id": id}
    values = {"$set": data}

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Card not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_query_card(id: str, current_user: User = Depends(get_current_active)):
    if (await db.delete_one(collection=collection, query={"_id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Card not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
