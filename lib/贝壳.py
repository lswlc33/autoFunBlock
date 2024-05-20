import requests
from lib.登录信息 import headers

session = requests.Session()
session.headers = headers


def 贝壳信息():
    response = requests.post(
        url="https://block-api.lucklyworld.com/v6/api/pets/shells/trade/index",
        headers=headers,
    )
    return response.json()


def 贝壳市场(type, page=1):
    """
    type: 0 求购中, 1 出售中
    """
    urls = [
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/purchase/list",
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/sale/list",
    ]

    url = urls[type]
    response = session.post(url=urls[type], data="page=1")
    return response.json()["list"]


def 贝壳交易(type, tradeId, quantity):
    """
    type: 0 购买, 1 出售
    tradeId: 交易id
    quantity: 数量
    """
    urls = [
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/purchase",
        "https://block-api.lucklyworld.com/v6/api/pets/shells/trade/sell",
    ]

    response = session.post(
        url=urls[type], data=f"tradeId={tradeId}&quantity={quantity}"
    )
    return response.json()