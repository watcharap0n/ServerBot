import json
from db import db
from fastapi import status
from fastapi.testclient import TestClient
from main import app, get_settings
from internal.config import Settings
import logging

client = TestClient(app)


def get_settings_override():
    return Settings(admin_email="wera.watcharapon@gmail.com")


app.dependency_overrides[get_settings] = get_settings_override

headers = {}
USER = {"username": "wera.watcharapon@gmail.com", "password": "kane!@#$"}

PAYLOAD_INTENT = {
    "name": "test unit",
    "access_token": "test unit access token",
    "ready": True,
    "status_flex": False,
    "content": "content test unit",
    "question": ["a", "b", "c", "d"],
    "answer": ["1", "2", "3", "4", "5"],
}


def get_token():
    token = client.post("/secure/token", data=USER)
    token = token.json()["access_token"]
    headers["Authorization"] = "Bearer " + token


def test_intent_create():
    get_token()
    response = client.post("/intents/create", json=PAYLOAD_INTENT, headers=headers)
    global ids_intent
    ids_intent = response.json()["_id"]
    assert response.status_code == status.HTTP_201_CREATED


def test_intent_duplicate():
    response = client.post("/intents/create", json=PAYLOAD_INTENT, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "item name duplicate"}


def test_intent_invalid():
    get_token()
    response = client.post(
        "/intents/create", json=PAYLOAD_INTENT.pop("name"), headers=headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "value is not a valid dict"


def test_intent_find():
    response = client.get(
        "/intents?access_token={}".format(PAYLOAD_INTENT.get("access_token")),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


def test_intent_find_empty():
    response = client.get("/intents?access_token=fake access token", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_intent_update():
    PAYLOAD_INTENT["name"] = "test update unit"
    response = client.put(
        f"/intents/query/update/{ids_intent}", json=PAYLOAD_INTENT, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


def test_intent_delete():
    response = client.delete(f"/intents/query/delete/{ids_intent}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


"""
Testing Intent success
"""

PAYLOAD_RuleBased = {
    "name": "test unit",
    "access_token": "test unit access token",
    "ready": True,
    "status_flex": False,
    "content": "content test unit",
    "question": ["a", "b", "c", "d"],
    "answer": ["1", "2", "3", "4", "5"],
}


def test_rule_based_create():
    get_token()
    response = client.post(
        "/rule_based/create", json=PAYLOAD_RuleBased, headers=headers
    )
    global ids_rule_based
    ids_rule_based = response.json()["_id"]
    assert response.status_code == status.HTTP_201_CREATED


def test_rule_based_duplicate():
    response = client.post(
        "/rule_based/create", json=PAYLOAD_RuleBased, headers=headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "item keyword duplicate"}


def test_rule_based_invalid():
    response = client.post(
        "/rule_based/create", json=PAYLOAD_RuleBased.pop("name"), headers=headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "value is not a valid dict"


def test_rule_based_find():
    response = client.get(
        "/rule_based?access_token={}".format(PAYLOAD_RuleBased.get("access_token")),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


def test_rule_based_find_empty():
    response = client.get("/rule_based?access_token=fake access token", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_rule_based_update():
    PAYLOAD_RuleBased["name"] = "test update unit"
    response = client.put(
        f"/rule_based/query/update/{ids_rule_based}",
        json=PAYLOAD_INTENT,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK


def test_rule_based_delete():
    response = client.delete(
        f"/rule_based/query/delete/{ids_rule_based}", headers=headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


"""
Testing RuleBased success
"""

# PAYLOAD_CALLBACK = {
#     'name': 'test unit name',
#     'access_token': 'test unit access token',
#     'secret_token': 'test unit secret token'
# }


# def test_callback_create():
#     response = client.post('/callback/channel/create', json=PAYLOAD_CALLBACK,
#                            headers=headers)
#     assert response.status_code == 200


# def test_callback_find():
#     channel = db.find_one(collection='webhook',
#                           query={'access_token': PAYLOAD_CALLBACK['access_token']})
#     uid = channel['uid']
#     response = client.get(f'/callback/channel/get?uid={uid}',
#                           headers=headers)
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# def test_callback_find_one():
#     access_token = PAYLOAD_CALLBACK['access_token']
#     response = client.get(f'/callback/channel/get/{access_token}',
#                           headers=headers)
#     assert response.status_code == 200


# def test_callback_find_one_not_found():
#     response = client.get(f'/callback/channel/get/fake_user_access_token',
#                           headers=headers)
#     assert response.status_code == 400


# def test_callback_delete():
#     channel = db.find_one(collection='webhook',
#                           query={'access_token': PAYLOAD_CALLBACK['access_token']})
#     token = channel['token']
#     response = client.delete(f'/callback/channel/delete/{token}',
#                              headers=headers)
#     assert response.status_code == 200
#     assert response.json() == {'detail': f'Delete success {token}'}


# """
# Testing Callback success
# """

# PAYLOAD_CARD = {
#     "name": "test unit name",
#     "content": "test unit content",
#     "message": "message"
# }


# def test_card_create():
#     response = client.post('/card/create', json=PAYLOAD_CARD,
#                            headers=headers)
#     assert response.status_code == 200


# def test_card_get():
#     response = client.get('/card', headers=headers)
#     assert response.status_code == 200


# def test_card_update():
#     card = db.find_one(collection='flex_message',
#                        query={'content': PAYLOAD_CARD['content']})
#     id_card = card['id']
#     PAYLOAD_CARD['name'] = 'test unit update name'
#     response = client.put(f'/card/query/update/{id_card}', json=PAYLOAD_CARD,
#                           headers=headers)
#     assert response.status_code == 200
#     assert {'detail': f'Update success {id_card}'}


# def test_card_delete():
#     card = db.find_one(collection='flex_message',
#                        query={'content': PAYLOAD_CARD['content']})
#     id_card = card['id']
#     response = client.delete(f'/card/query/delete/{id_card}',
#                              headers=headers)
#     assert response.status_code == 200
#     assert response.json() == {'detail': f'Delete success {id_card}'}
