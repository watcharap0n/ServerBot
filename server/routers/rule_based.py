from db import db
from typing import Optional, List
from starlette.responses import JSONResponse
from models.rule_based import RuleBased, TokenUser, UpdateRuleBased
from modules.item_static import item_user
from oauth2 import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = "rule_based"


async def check_rule_based_duplicate(rule_based: RuleBased):
    item = await db.find_one(
        collection=collection,
        query={"access_token": rule_based.access_token, "keyword": rule_based.keyword}
    )
    if item:
        if item.get('keyword') is None or not item.get('keyword'):
            return rule_based
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid duplicate keyword."
        )
    return rule_based


@router.get("/", response_model=List[TokenUser])
async def get_rule_based(
        access_token: Optional[str] = None, current_user: User = Depends(get_current_active)
):
    items = await db.find(collection=collection, query={"access_token": access_token})
    items = list(items)
    return items


@router.post("/create", response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def create_rule_based(
        rule_based: RuleBased = Depends(check_rule_based_duplicate),
        current_user: User = Depends(get_current_active),
):
    item_model = jsonable_encoder(rule_based)
    item_model = item_user(data=item_model, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenUser(**item_model)
    return item_store


@router.put("/query/update/{id}", response_model=UpdateRuleBased)
async def update_query_rule_based(
        id: str, payload: UpdateRuleBased, current_user: User = Depends(get_current_active)
):
    data = jsonable_encoder(payload)
    query = {"_id": id}
    values = {"$set": data}

    if payload.status_flex:
        if (await db.find_one(collection='card', query={'_id': payload.card})) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'id card not found {payload.card}')

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Rule Based not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}")
async def delete_query_rule_based(
        id: str, current_user: User = Depends(get_current_active)
):
    if (await db.delete_one(collection=collection, query={"_id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Rule Based not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
