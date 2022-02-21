import json
from db import db
from numpy import random
from pydantic import BaseModel
from starlette.responses import JSONResponse
from modules.item_static import item_user
from modules.flex_message import flex_dynamic
from models.callback import Webhook, LineToken, UpdateLineToken
from random import randint
from typing import Optional, List
from fastapi import APIRouter, Depends, Body, Request, status, HTTPException, Path
from oauth2 import get_current_active, User
from fastapi.encoders import jsonable_encoder
from linebot import LineBotApi, WebhookHandler
from linebot.models import StickerSendMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from modules.mg_chatbot import chatbot_standard, intent_model
from linebot.exceptions import InvalidSignatureError, LineBotApiError

router = APIRouter()
collection = "webhook"


async def get_webhook(token):
    user = await db.find_one(collection=collection, query={"token": token})
    user = Webhook(**user)
    return user


def create_file_json(path: str, data):
    with open(path, mode="w") as jsonfile:
        json.dump(data, jsonfile)


async def get_profile(userId: str, access_token: str):
    line_bot_api = LineBotApi(access_token)
    profile = line_bot_api.get_profile(userId)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    result = {
        "displayName": displayName,
        "userId": userId,
        "img": img,
        "status": status,
    }
    return result


async def check_access_token(item: LineToken):
    user = await db.find_one(
        collection=collection, query={"access_token": item.access_token}
    )
    if not user:
        try:
            line_bot_api = LineBotApi(item.access_token)
            line_bot_api.get_bot_info()
            return item
        except LineBotApiError as ex:
            raise HTTPException(status_code=ex.status_code, detail=ex.message)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Access token have already",
    )


@router.get("/channel/info", response_model=List[Webhook])
async def get_all_token(current_user: User = Depends(get_current_active)):
    """

    :param uid:
    :param current_user:
    :return:
    """
    uid = current_user.data.uid
    channels = await db.find(collection=collection, query={"uid": uid})
    channels = list(channels)
    return channels


@router.get("/channel/info/{token}", response_model=Webhook)
async def get_query_token(token: str,
                          current_user: User = Depends(get_current_active)):
    channel = await db.find_one(collection=collection, query={"token": token})
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"not found channel {token}",
        )

    channel = Webhook(**channel)
    return channel


@router.post("/channel/create", response_model=Webhook)
async def create_channel(
        item: LineToken = Depends(check_access_token),
        current_user: User = Depends(get_current_active),
):
    """

    :param item:
    :param current_user:
    :return:
    """

    line_bot_api = LineBotApi(item.access_token)
    bot_info = line_bot_api.get_bot_info()
    item_model = jsonable_encoder(item)
    item_model = item_user(data=item_model, current_user=current_user, url=True)
    item_model["bot_info"] = bot_info
    item_model = jsonable_encoder(item_model)
    store_model = Webhook(**item_model)
    await db.insert_one(collection=collection, data=item_model)
    return store_model


@router.put("/channel/update/{token}", response_model=UpdateLineToken)
async def update_channel(
        payload: UpdateLineToken,
        token: Optional[str] = None,
        current_user: User = Depends(get_current_active),
):
    try:
        line_bot_api = LineBotApi(payload.access_token)
        line_bot_api.get_bot_info()
        data = jsonable_encoder(payload)
        query = {"token": token}
        values = {"$set": data}

        if (await db.update_one(collection=collection, query=query, values=values)) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Callback not found {token} or Update Already exits",
            )
        return payload
    except LineBotApiError as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)


@router.delete("/channel/delete/{token}")
async def delete_channel(
        token: Optional[str] = None, current_user: User = Depends(get_current_active)
):
    """

    :param token:
    :param current_user:
    :return:
    """
    if (await db.delete_one(collection=collection, query={"token": token})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Callback not found {token} or Delete Already exits",
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{token}")
async def client_webhook(
        request: Request,
        token: Optional[str] = Path(...),
        payload: Optional[dict] = Body(None),
):
    """

    :param request:
    :param token:
    :param payload:
    :return:
    """

    model = await get_webhook(token)
    handler = WebhookHandler(model.secret_token)
    create_file_json("static/log/line.json", payload)
    try:
        signature = request.headers['X-Line-Signature']
        body = await request.body()
        events = payload["events"][0]
        event_type = events["type"]
        if event_type == "follow":
            userId = events["source"]["userId"]
            follower = await get_profile(userId, model.access_token)
            db.insert_one(collection="follower_linebot", data=follower)
        elif event_type == "unfollow":
            userId = events["source"]["userId"]
            db.delete_one("follower_linebot", query={"userId": userId})
        elif event_type == "postback":
            event_postback(events, model)
        elif event_type == "message":
            message_type = events["message"]["type"]
            if message_type == "text":
                try:
                    userId = events["source"]["userId"]
                    message = events["message"]["text"]
                    profile = await get_profile(userId, model.access_token)
                    profile["message"] = message
                    await db.insert_one(collection="message_user", data=profile)
                    handler.handle(str(body, encoding='utf8'), signature)
                    await handler_message(events, model)
                except InvalidSignatureError as v:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={"status_code": 400, "message": v.message},
                    )
            else:
                no_event = len(payload["events"])
                for i in range(no_event):
                    events = payload["events"][i]
                    event_handler(events, model)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail={"message": "Index error"}
        )
    return payload


def event_postback(events, model):
    pass


def event_handler(events, model):
    line_bot_api = LineBotApi(model.access_token)
    replyToken = events["replyToken"]
    package_id = "446"
    stickerId = randint(1988, 2027)
    line_bot_api.reply_message(
        replyToken, StickerSendMessage(package_id, str(stickerId))
    )


def quick_reply_custom(line_bot_api, userId: str, send_text: str, labels: list, texts: list):
    line_bot_api.reply_message(
        userId,
        TextSendMessage(
            text=send_text,
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=label, text=text)) for label, text in zip(labels, texts)
            ])
        )
    )


async def get_card_content(card):
    content_card = await db.find_one(collection='card', query={'_id': card})
    content = json.loads(content_card.get('content'))
    flex_msg = flex_dynamic(alt_text=content_card.get('name'), contents=content)
    return flex_msg


class Word(BaseModel):
    X: list
    y: list
    answers: Optional[list] = None


def preprocessing_words(db):
    sum_word = []
    ans_list = [x['answer'] for x in db]
    embedding = [x for x in range(len(ans_list))]
    for words in db:
        text = str()
        for word in words['question']:
            text += word
        sum_word.append(text)
    return Word(X=sum_word, y=embedding, answers=ans_list)


def iterate_item(items: list, condition: str, match: str) -> dict:
    for item in items:
        if item.get(condition) == match:
            return item


async def handler_message(events, model):
    line_bot_api = LineBotApi(model.access_token)
    message = events["message"]["text"]
    reply_token = events["replyToken"]

    items_keyword = await db.find(collection='rule_based', query={'access_token': model.access_token})
    keyword = iterate_item(items=items_keyword, condition='keyword', match=message)

    if not keyword:
        intents = list(await db.find(collection='intents', query={'access_token': model.access_token}))
        words = preprocessing_words(db=intents)
        result_intent = await intent_model(
            X=words.X,
            y=words.y,
            answers=words.answers,
            message=message,
            db=intents
        )
        if result_intent.get('require'):
            line_bot_api.reply_message(reply_token, TextSendMessage(text=result_intent.get('require')))

        confidence = result_intent.get('confidence')[0] * 100
        status_flex = result_intent['status_flex']
        predicted = result_intent['predicted'][0]
        answers = result_intent['answers']
        card = result_intent['card']
        ready = result_intent['ready']
        id_intent = result_intent['id']

        buttons = await db.find_one(collection='quick_reply', query={'intent': id_intent})
        if buttons:
            labels = buttons['labels']
            texts = buttons['texts']
            reply_message = buttons['reply']
            reply = random.choice(reply_message)
            quick_reply_custom(line_bot_api, reply_token, reply, labels, texts)

        elif not buttons:
            if ready:
                if confidence > 69:
                    if status_flex:
                        flex_msg = await get_card_content(card)
                        line_bot_api.reply_message(reply_token, flex_msg)

                    elif not status_flex:
                        reply = random.choice(answers[predicted])
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=reply))
                else:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text='.'))

    elif keyword:
        answer_keyword = keyword.get('answer')
        card_keyword = keyword.get('card')
        if keyword.get('ready'):
            if keyword.get('status_flex'):
                flex_msg = await get_card_content(card_keyword)
                line_bot_api.reply_message(reply_token, flex_msg)

            elif not keyword.get('status_flex'):
                reply = random.choice(answer_keyword)
                line_bot_api.reply_message(reply_token, TextSendMessage(text=reply))
