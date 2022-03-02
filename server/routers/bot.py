from typing import List
from db import db
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from oauth2 import get_current_active, User
from fastapi import APIRouter, Depends, HTTPException, status
from modules.flex_message import flex_dynamic, content_card_dynamic
from models.bot import (MessageFactory, PushMessage, PushFlex, PushFlexDefault, PushImage, PushSticker)
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage

router = APIRouter()


@router.get('/chat/list', response_model=List[MessageFactory])
async def chat_list(access_token: str, current_user: User = Depends(get_current_active)):
    items = await db.find(collection='messages_user', query={'access_token': access_token})
    return items


async def check_access_token(payload,
                             current_user: User = Depends(get_current_active)):
    try:
        line_bot_api = LineBotApi(payload.access_token)
        line_bot_api.get_bot_info()
        return payload
    except LineBotApiError as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)


@router.post('/push/message', response_model=PushMessage)
async def push_message(payload: PushMessage = Depends(check_access_token),
                       current_user: User = Depends(get_current_active)):
    line_bot_api = LineBotApi(payload.access_token)
    line_bot_api.push_message(payload.user_id, TextSendMessage(text=payload.message))


async def query_card(payload: PushFlex = Depends(check_access_token),
                     current_user: User = Depends(get_current_active)):
    item = await db.find_one(collection='card', query={'uid': current_user.data.uid,
                                                       '_id': payload.id_card})
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Flex not found')
    payload = PushFlex(id_card=item.get('content'))
    return payload


@router.post('/push/flex/any', response_model=PushFlex)
async def push_flex(payload: PushFlex = Depends(check_access_token),
                    current_user: User = Depends(get_current_active)):
    line_bot_api = LineBotApi(payload.access_token)
    line_bot_api.push_message(payload.user_id, payload.content)


@router.post('/push/flex/defalut', response_model=PushFlexDefault)
async def push_flex_default(payload: PushFlexDefault = Depends(check_access_token),
                            current_user: User = Depends(get_current_active)):
    keys = payload.content.keys()
    values = payload.content.values()
    content_default = payload.config_default_card
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
    line_bot_api = LineBotApi(payload.access_token)
    line_bot_api.push_message(payload.user_id, func)
    return PushFlexDefault


@router.post('/push/image', response_model=PushImage)
async def push_image(payload: PushImage = Depends(check_access_token)):
    line_bot_api = LineBotApi(payload.access_token)
    line_bot_api.push_message(payload.user_id, ImageSendMessage(
        original_content_url=payload.image_original,
        preview_image_url=payload.image_preview,
    ))
    return PushImage


@router.post('/push/sticker', response_model=PushSticker)
async def push_sticker(payload: PushSticker = Depends(check_access_token)):
    line_bot_api = LineBotApi(payload.access_token)
    line_bot_api.push_message(payload.user_id, StickerSendMessage(
        sticker_id=payload.sticker_id,
        package_id=payload.package_id
    ))
