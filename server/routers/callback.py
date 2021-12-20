import json
from random import randint
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Body, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from routers.secure import get_current_active, User
from fastapi.encoders import jsonable_encoder
from internal import db, Id
from linebot import LineBotApi, WebhookHandler
from linebot.models import StickerSendMessage
from linebot.exceptions import InvalidSignatureError

router = APIRouter()
collection = 'follwer_linebot'


class CreateWebhook(BaseModel):
    access_token: str = Field(..., example='channel access token long live')
    secret_token: str = Field(..., example='channel secret token webhook')


class ModelWebhook(CreateWebhook):
    uid: Optional[str] = None
    url: Optional[str] = None
    token: Optional[str] = None


def get_webhook(token):
    user = db.find_one(collection='webhook',
                       query={'token': token})
    user = ModelWebhook(**user)
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


@router.post('/webhook/create', response_model=CreateWebhook)
async def create_url_webhook(item: CreateWebhook,
                             current_user: User = Depends(get_current_active)):
    item_model = jsonable_encoder(item)
    item_model['url'] = f'https://mangoserverbot.herokuapp.com/callback/{Id}'
    item_model['uid'] = current_user.data.uid
    item_model['token'] = Id
    db.insert_one(collection='webhook', data=item_model)
    return item_model


@router.post('/{token}/')
async def client_webhook(
        request: Request,
        token: str,
        payload: Optional[dict] = Body(None),
):
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


def event_handler(events, model):
    line_bot_api = LineBotApi(model.access_token)
    replyToken = events['replyToken']
    package_id = '446'
    stickerId = randint(1988, 2027)
    line_bot_api.reply_message(replyToken, StickerSendMessage(package_id, str(stickerId)))


def handler_message(events, model):
    pass


def event_postback(events, model):
    pass
