import json
from typing import List
from db import db
from linebot import LineBotApi
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


@router.post('/push/message', response_model=PushMessage)
async def push_message(payload: PushMessage,
                       current_user: User = Depends(get_current_active)):
    line_bot_api = LineBotApi(payload.access_token)
    message = TextSendMessage(text=payload.message)
    if payload.broadcast:
        line_bot_api.broadcast(message)
        return payload
    if payload.multicast:
        line_bot_api.multicast(payload.user_id, message)
        return payload
    line_bot_api.push_message(payload.user_id[0], message)
    return payload


async def query_card(payload: PushFlex,
                     current_user: User = Depends(get_current_active)):
    item = await db.find_one(collection='card', query={'uid': current_user.data.uid,
                                                       '_id': payload.id_card})
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Flex not found')
    payload = PushFlex(id_card=item.get('content'))
    return payload


@router.post('/push/flex/any', response_model=PushFlex)
async def push_flex(payload: PushFlex = Depends(query_card),
                    current_user: User = Depends(get_current_active)):
    line_bot_api = LineBotApi(payload.access_token)
    flex = json.loads(payload.id_card)
    if payload.broadcast:
        line_bot_api.broadcast(flex_dynamic(flex))
        return payload
    if payload.multicast:
        line_bot_api.multicast(payload.user_id, flex)
        return payload
    line_bot_api.push_message(payload.user_id[0], flex)
    return payload


@router.post('/push/flex/default', response_model=PushFlexDefault)
async def push_flex_default(payload: PushFlexDefault,
                            current_user: User = Depends(get_current_active)):
    keys = payload.content.keys()
    values = payload.content.values()
    content_default = payload.config_default_card
    func, content = content_card_dynamic(
        header=content_default.header,
        image=content_default.image,
        path_image=content_default.path_image,
        footer=content_default.footer,
        body_key=keys,
        body_value=values,
        name_btn=content_default.name_btn,
        url_btn=content_default.url_btn
    )
    line_bot_api = LineBotApi(payload.access_token)
    if payload.broadcast:
        line_bot_api.broadcast(func)
        return payload
    if payload.multicast:
        line_bot_api.multicast(payload.user_id, func)
        return payload
    line_bot_api.push_message(payload.user_id[0], func)
    return payload


@router.post('/push/image', response_model=PushImage)
async def push_image(payload: PushImage,
                     current_user: User = Depends(get_current_active)):
    line_bot_api = LineBotApi(payload.access_token)
    image = ImageSendMessage(
        original_content_url=payload.image_original,
        preview_image_url=payload.image_preview,
    )
    if payload.broadcast:
        line_bot_api.broadcast(image)
        return payload
    if payload.multicast:
        line_bot_api.multicast(payload.user_id, image)
        return payload
    line_bot_api.push_message(payload.user_id[0], image)
    return payload


@router.post('/push/sticker', response_model=PushSticker)
async def push_sticker(payload: PushSticker,
                       current_user: User = Depends(get_current_active)):
    line_bot_api = LineBotApi(payload.access_token)
    sticker = StickerSendMessage(
        sticker_id=payload.sticker_id,
        package_id=payload.package_id
    )
    if payload.broadcast:
        line_bot_api.broadcast(sticker)
        return payload
    if payload.multicast:
        line_bot_api.multicast(payload.user_id, sticker)
        return payload
    line_bot_api.push_message(payload.user_id[0], sticker)
    return payload
