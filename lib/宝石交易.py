from requests import Session
from lib.登录信息 import headers

session = Session()
session.headers = headers


def get_gift_logs(page=0):
    # 获取赠送记录
    return session.post(
        url="https://block-api.lucklyworld.com/v11/api/ba/rocks/transfer/logs",
        data=f"page={page}",
    ).json()
