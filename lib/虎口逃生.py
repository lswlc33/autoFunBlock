from requests import session
from lib.登录信息 import headers


session = session()
session.headers = headers


def escape_placing(propId, num=1):
    return session.post(
        url="https://block-api.lucklyworld.com/v6/api/ba/escape/placing/prop/v2",
        data=f"propId={propId}&num={num}",
    ).json()


def escape_participate(animalId):
    return session.post(
        url="https://block-api.lucklyworld.com/v6/api/ba/escape/participate",
        data=f"animalId={animalId}",
    ).json()


def escape_polling():
    return session.post(
        url="https://block-api.lucklyworld.com/v6/api/ba/escape/index/polling",
        data="lastBarrageId=147767645",
    ).json()


def escape_run_list():
    return session.post(
        url="https://block-api.lucklyworld.com/v6/api/ba/escape/run/list",
    ).json()
