import requests
import json
from 登录信息 import headers

def 游戏入场(筹码):

    url = "https://block-api.lucklyworld.com/v11/api/multi/game/start"

    payload = f"multi={筹码}"

    response = requests.post(url, data=payload, headers=headers)

    print(response.json())


def 游戏提交():

    url = "https://block-api.lucklyworld.com/v11/api/multi/game/chess/select"

    payload = json.dumps(
        {
            "indexIdArr": [
                81,
                82,
                83,
                84,
                85,
                86,
                87,
                88,
                89,
                80,
                79,
                78,
                77,
                76,
                75,
                74,
                73,
                72,
                63,
                64,
                65,
                66,
                67,
                68,
                69,
                70,
                71,
                62,
                61,
                60,
                59,
                58,
                57,
                56,
                55,
                54,
                45,
                46,
                47,
                48,
                49,
                50,
                51,
                52,
                53,
            ]
        }
    )

    response = requests.post(url, data=payload, headers=headers)

    print(response.json())


def 游戏结算():
    url = "https://block-api.lucklyworld.com/v11/api/multi/game/end"

    response = requests.post(url, headers=headers)

    print(response.json())
