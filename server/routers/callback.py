import json
from datetime import datetime
from random import randint
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Body, Request, status, HTTPException
from routers.secure import get_current_active, User
from fastapi.encoders import jsonable_encoder
from db import db, generate_token
from linebot import LineBotApi, WebhookHandler
from linebot.models import StickerSendMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

router = APIRouter()
collection = 'webhook'


class LineToken(BaseModel):
    name: str = Field(..., example='name line official')
    access_token: str = Field(..., example='channel access token long live')
    secret_token: str = Field(..., example='channel secret token webhook')


class Webhook(LineToken):
    uid: Optional[str] = None
    url: Optional[str] = None
    token: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None


class ListWebhook(BaseModel):
    __root__: List[Webhook]


def get_webhook(token):
    user = db.find_one(collection=collection,
                       query={'token': token})
    user = Webhook(**user)
    return user


def create_file_json(path: str, data):
    with open(path, mode='w') as jsonfile:
        json.dump(data, jsonfile)


def get_profile(userId: str, access_token: str) -> dict:
    line_bot_api = LineBotApi(access_token)
    profile = line_bot_api.get_profile(userId)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    result = {'displayName': displayName, 'userId': userId, 'img': img, 'status': status}
    return result


async def check_access_token(item: LineToken):
    user = db.find_one(collection=collection, query={'access_token': item.access_token})
    if not user:
        return item
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail={'message': 'Access token have already', 'data': user})


@router.get('/channel/get', response_model=ListWebhook)
async def get_all_token(uid: Optional[str] = None,
                        current_user: User = Depends(get_current_active)):
    """

    :param uid:
    :param current_user:
    :return:
    """
    user = db.find(collection=collection, query={'uid': uid})
    user = list(user)
    channels = ListWebhook.parse_obj(user)
    return channels


@router.get('/channel/get/{access_token}', response_model=Webhook)
async def get_query_token(access_token: str):
    channel = db.find_one(collection=collection, query={'access_token': access_token})
    if not channel:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='not found channel')
    channel = Webhook(**channel)
    return channel


@router.post('/channel/create', response_model=Webhook)
async def create_channel(item: LineToken = Depends(check_access_token),
                         current_user: User = Depends(get_current_active)):
    """

    :param item:
    :param current_user:
    :return:
    """
    Id = generate_token(engine=ObjectId())
    _d = datetime.now()
    item_model = jsonable_encoder(item)
    item_model['url'] = f'https://mangoserverbot.herokuapp.com/callback/{Id}'
    item_model['uid'] = current_user.data.uid
    item_model['token'] = Id
    item_model["date"] = _d.strftime("%d/%m/%y")
    item_model["time"] = _d.strftime("%H:%M:%S")
    db.insert_one(collection=collection, data=item_model)
    store_model = Webhook(**item_model)
    return store_model


@router.delete('/channel/delete/{token}')
async def delete_channel(token: Optional[str] = None,
                         current_user: User = Depends(get_current_active)):
    """

    :param token:
    :param current_user:
    :return:
    """
    db.delete_one(collection=collection, query={'token': token})
    return {'detail': f'Delete success {token}'}


@router.post('/{token}')
async def client_webhook(
        request: Request,
        token: str,
        payload: Optional[dict] = Body(None),
):
    """

    :param request:
    :param token:
    :param payload:
    :return:
    """
    model = get_webhook(token)
    handler = WebhookHandler(model.secret_token)
    create_file_json('static/log/line.json', payload)
    try:
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        events = payload['events'][0]
        event_type = events['type']
        if event_type == 'follow':
            userId = events['source']['userId']
            follower = get_profile(userId, model.access_token)
            db.insert_one(collection='follower_linebot', data=follower)
        elif event_type == 'unfollow':
            userId = events['source']['userId']
            db.delete_one('follower_linebot', query={'userId': userId})
        elif event_type == 'postback':
            event_postback(events, model)
        elif event_type == 'message':
            message_type = events['message']['type']
            if message_type == 'text':
                try:
                    userId = events['source']['userId']
                    message = events['message']['text']
                    profile = get_profile(userId, model.access_token)
                    profile['message'] = message
                    db.insert_one(collection='message_user', data=profile)
                    handler.handle(str(body, encoding='utf8'), signature)
                    handler_message(events, model)
                except InvalidSignatureError as v:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={'status_code': v.status_code, 'message': v.message}
                    )
            else:
                no_event = len(payload['events'])
                for i in range(no_event):
                    events = payload['events'][i]
                    event_handler(events, model)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_200_OK, detail={'message': 'Index error'})
    return payload


def event_postback(events, model):
    pass


def event_handler(events, model):
    line_bot_api = LineBotApi(model.access_token)
    replyToken = events['replyToken']
    package_id = '446'
    stickerId = randint(1988, 2027)
    line_bot_api.reply_message(replyToken, StickerSendMessage(package_id, str(stickerId)))


def handler_message(events, model):
    line_bot_api = LineBotApi(model.access_token)
    text = events['message']['text']
    reply_token = events['replyToken']
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
