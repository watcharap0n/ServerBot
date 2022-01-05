"""
def function -> static item model
    - id
    - date
    - time
    - uid
"""
from bson import ObjectId
import logging
from typing import Optional
from datetime import datetime
from db import generate_token


def item_user(data: dict, current_user,
               change_id: Optional[str] = None) -> dict:
    """

    :param change_id:
    :param data:
    :param current_user:
    :return:
    """

    try:
        Id = generate_token(engine=ObjectId())
        _d = datetime.now()
        data['id'] = Id
        data['uid'] = current_user.data.uid
        data["date"] = _d.strftime("%d/%m/%y")
        data["time"] = _d.strftime("%H:%M:%S")
        return data
    except KeyError:
        raise logging.exception('your key error')
    except Exception:
        raise logging.exception('something error')
