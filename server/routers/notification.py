import json
from db import db
from linebot import LineBotApi
from models.notification import Post, TokenUser
from oauth2 import User, get_current_active
from fastapi import APIRouter, HTTPException, Depends, status
from modules.item_static import item_user
from modules.flex_message import flex_dynamic, content_card_dynamic
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = 'notifications'


async def check_access_token(payload: Post,
                             current_user: User = Depends(get_current_active)):
    try:
        line_bot_api = LineBotApi(payload.access_token)
        line_bot_api.get_bot_info()
        return payload
    except LineBotApiError as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)


async def post_content(payload: Post = Depends(check_access_token),
                       current_user: User = Depends(get_current_active)):
    local_collection = 'card'
    line_bot_api = LineBotApi(payload.access_token)

    if payload.flex_status:
        if payload.id_card:
            card = await db.find_one(collection=local_collection,
                                     query={'uid': current_user.data.uid, '_id': payload.id_card})
            if not card:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={f'not found id card {payload.id_card}'})
            elif card:
                content = json.loads(card.get('content'))
                flex_msg = flex_dynamic(alt_text=card.get('name'), contents=content)
                line_bot_api.push_message(payload.user_id, flex_msg)
        return payload

    line_bot_api.push_message(payload.user_id, TextSendMessage(text=payload.message))
    item_model = jsonable_encoder(payload)
    item_model = item_user(data=item_model, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenUser(**item_model)
    return item_store


@router.post('/post/any', response_model=TokenUser)
async def post_any(notify: Post = Depends(post_content),
                   current_user: User = Depends(get_current_active)):
    keys = notify.content.keys()
    values = notify.content.values()
    content_default = notify.config_default_card
    func, content = content_card_dynamic(
        header=content_default.get('header'),
        image=content_default.get('image'),
        path_image=content_default.get('path_image'),
        footer=content_default.get('footer'),
        body_key=keys,
        body_value=values,
        name_btn=content_default.get('name_btn'),
        url_btn=content_default.get('url_btn')
    )
    line_bot_api = LineBotApi(notify.access_token)
    line_bot_api.push_message(notify.user_id, func)
    item_model = jsonable_encoder(notify)
    item_model = item_user(data=item_model, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenUser(**item_model)
    return item_store
