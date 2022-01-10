"""
def function -> static item model
    - id
    - date
    - time
    - uid
"""
import logging
from typing import Optional
from datetime import datetime


def item_user(data: dict, current_user, url: Optional[bool] = False):
    """

    :param change_id:
    :param data:
    :param current_user:
    :return:
    """

    try:
        _d = datetime.now()
        data["uid"] = current_user.data.uid
        data["date"] = _d.strftime("%d/%m/%y")
        data["time"] = _d.strftime("%H:%M:%S")
        if url:
            data[
                "url"
            ] = f"https://mangoserverbot.herokuapp.com/callback/{data['token']}"
        return data
    except KeyError:
        raise logging.exception("your key error")
    except Exception:
        raise logging.exception("something error")
