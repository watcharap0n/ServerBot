from fastapi import APIRouter
from typing import Optional
from models.user import User
import json

router = APIRouter()


def read_json_marketing(path: str):
    with open(path, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data


def sorting_id(elem):
    return elem.get('ID')


@router.get('/')
async def read_customers(q: Optional[int] = None, check: Optional[str] = None):
    data = read_json_marketing('static/json/data_customers.json')
    if q:
        for cust in data:
            if q == cust['ID']:
                description = {'message': 'success read!', 'status': True}
                cust['metadata'] = description
                return cust
        return {'metadata': {'message': 'invalid id not found!', 'status': False}}
    elif check:
        if check == 'lasted':
            data.sort(key=sorting_id)
            cust = data[-1]
            description = {'message': 'success read query!', 'status': True}
            cust['metadata'] = description
            return cust
    elif q is None and check is None:
        return data


@router.post('/', status_code=201, response_model=User)
async def add_customer(payload: User):
    payload = payload.dict()
    data = read_json_marketing('static/json/data_customers.json')
    data.sort(key=sorting_id)
    id_lasted = data[-1]['ID'] + 1
    payload['ID'] = id_lasted
    data.append(payload)
    with open('static/json/data_customers.json', 'w') as jsonfile:
        json.dump(data, jsonfile)
    return payload


@router.put('/{id_cust}')
async def update_customer(payload: User, id_cust: Optional[int] = None):
    data = read_json_marketing('static/json/data_customers.json')
    for cust in data:
        if cust['ID'] == id_cust:
            cust.update(payload)
    with open('static/json/data_customers.json', 'w') as jsonfile:
        json.dump(data, jsonfile)
    return {'message': 'success updated!', 'status': True}


@router.delete('/{id_cust}')
async def delete_customer(id_cust: Optional[int] = None):
    data = read_json_marketing('static/json/data_customers.json')
    for cust in data:
        if cust['ID'] == id_cust:
            data.remove(cust)
    with open('static/json/data_customers.json', 'w') as jsonfile:
        json.dump(data, jsonfile)
    return {'message': 'success deleted!', 'status': True}
