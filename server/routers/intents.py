from db import db
from typing import Optional, List
from starlette.responses import JSONResponse
from models.intent import Intent, TokenUser, UpdateIntent
from modules.item_static import item_user
from oauth2 import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = "intents"


async def check_intent_duplicate(intent: Intent):
    item = await db.find_one(
        collection=collection,
        query={"access_token": intent.access_token, "name": intent.name}
    )
    if item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid duplicate name."
        )
    return intent


@router.get("/", response_model=List[TokenUser])
async def get_intents(
        access_token: Optional[str] = None,
        current_user: User = Depends(get_current_active)
):
    items = await db.find(collection=collection, query={"access_token": access_token})
    items = list(items)
    return items


@router.post("/create", response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def create_intents(
        intent: Intent = Depends(check_intent_duplicate),
        current_user: User = Depends(get_current_active),
):
    item_model = jsonable_encoder(intent)
    item_model = item_user(data=item_model, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenUser(**item_model)
    return item_store


@router.put("/query/update/{id}", response_model=UpdateIntent)
async def update_query_intent(
        id: str, payload: UpdateIntent,
        current_user: User = Depends(get_current_active)
):
    data = jsonable_encoder(payload)
    query = {"_id": id}
    values = {"$set": data}

    if payload.status_flex:
        if (await db.find_one(collection='card', query={'_id': payload.card})) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'id card not found {payload.card}')

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Intent not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_query_intent(
        id: str, current_user: User = Depends(get_current_active)
):
    if (await db.delete_one(collection=collection, query={"_id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Intent not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
