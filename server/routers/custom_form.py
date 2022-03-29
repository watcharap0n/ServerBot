from db import db
from typing import Optional, List
from oauth2 import get_current_active, User
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from modules.item_static import item_user
from models.custom_form import CustomForm, TokenUser, UpdateForm

router = APIRouter()

collection = 'form'


@router.get('/find', response_model=List[TokenUser])
async def get_form(
        access_token: Optional[str] = None,
        current_user: User = Depends(get_current_active)
):
    items = await db.find(collection=collection, query={"access_token": access_token})
    items = list(items)
    return items


async def check_duplicate_id_form(form: CustomForm):
    item = await db.find_one(collection=collection,
                             query={"access_token": form.access_token, "id_form": form.id_form}
                             )
    if item:
        if item.get('id_form') is None or not item.get('id_form'):
            return form
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid duplicate id_form."
        )
    return form


@router.get('/find/{id}', response_model=TokenUser)
async def get_form_one(id: str):
    item = await db.find_one(collection=collection, query={'_id': id})
    return item


@router.post("/create", response_model=TokenUser, status_code=status.HTTP_201_CREATED)
async def create_form(
        form: CustomForm = Depends(check_duplicate_id_form),
        current_user: User = Depends(get_current_active),
):
    item_model = jsonable_encoder(form)
    item_model['endpoint'] = "/form/custom/" + item_model['_id']
    item_model = item_user(item_model, current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenUser(**item_model)
    return item_store


@router.put("/query/update/{id}", response_model=UpdateForm)
async def update_form(
        id: str,
        payload: UpdateForm,
        current_user: User = Depends(get_current_active)
):
    data = jsonable_encoder(payload)
    query = {"_id": id}
    values = {"$set": data}

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Form not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(
        id: str,
        current_user: User = Depends(get_current_active)
):
    if (await db.delete_one(collection=collection, query={"_id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Form not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
