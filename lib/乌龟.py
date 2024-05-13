import requests
from lib.登录信息 import headers

session = requests.Session()


def 召回显示乌龟(state, petId):
    """
    召回显示乌龟
    state: 1 显示 0 隐藏
    petId: 乌龟ID
    """
    url = "https://block-api.lucklyworld.com/v6/api/blockbeast/pets/desktop/display"
    payload = f"state={state}&petId={petId}"
    response = session.post(url, data=payload, headers=headers)
    print(response.json())


def 获取乌龟信息():
    url = "https://block-api.lucklyworld.com/v6/api/blockbeast/pets/index"

    response = session.post(url, headers=headers)

    data = response.json()

    res = {
        # 乌龟ID
        "id": data["id"],
        "sn": data["sn"],
        # 我的资产
        "rocks": data["rocks"],
        "shells": data["shells"],
        # 今日获取
        "todayRocks": data["pickup"]["rocks"]["today"],
        "todayShells": data["pickup"]["shell"]["today"],
        # 乌龟性别
        "gender": data["gender"],
        # 乌龟等级
        "level": data["level"],
        "levelProgress": data["levelProgress"],
        # 乌龟代数
        "generation": data["generation"],
        # 乌龟属性
        "combatPower": data["attribute"]["combatPower"],
        "stamina": data["attribute"]["stamina"],
        "speed": data["attribute"]["speed"],
        "strength": data["attribute"]["strength"],
        "luck": data["attribute"]["luck"],
        # 乌龟状态
        "hunger": data["hunger"]["currentVal"],
        "cleanliness": data["cleanliness"]["currentVal"],
        "healthiness": data["healthiness"]["currentVal"],
        # 探测器
        "detector": data["detector"]["level"],
        "desktopDisplay": data["desktopDisplay"],
    }
    return res


def 升级探测器():
    url = "https://block-api.lucklyworld.com/v6/api/pets/detector/upgrade"

    response = session.post(url, headers=headers)

    print(response.json())


def 乌龟清理(petId):
    response = session.post(
        url="https://block-api.lucklyworld.com/v6/api/blockbeast/pets/clean",
        data=f"petId={petId}",
        headers=headers,
    )

    print(response.json())


def 乌龟喂养(petId):
    response = session.post(
        url="https://block-api.lucklyworld.com/v6/api/blockbeast/pets/feed",
        data=f"petId={petId}",
        headers=headers,
    )

    print(response.json())


def 捡起宝石():
    url = "https://block-api.lucklyworld.com/v6/api/pets/pickup/rocks"
    response = session.post(url, headers=headers)
    return response.json()


def 宠物心跳():
    url = "https://block-api.lucklyworld.com/v6/api/blockbeast/pets/desktop/ping"
    response = session.post(url, headers=headers)
    return response.json()


def 捡宝历史():
    url = "https://block-api.lucklyworld.com/v6/api/pets/pickup/rocks/logs"
    response = session.post(url, headers=headers)
    return response.json()


if __name__ == "__main__":
    data = {
        "petId": 209681,
        "total": "15.2756",
        "totalShells": "2140.66",
        "tips": "每五分钟更新一次数据",
        "list": [
            {
                "date": "2024-05-09",
                "duration": "17小时59分钟",
                "amount": "1.1891",
                "shells": "426.04",
            },
            {
                "date": "2024-05-08",
                "duration": "18小时45分钟",
                "amount": "1.5455",
                "shells": "427.67",
            },
            {
                "date": "2024-05-07",
                "duration": "19小时35分钟",
                "amount": "1.5060",
                "shells": "437.41",
            },
            {
                "date": "2024-05-06",
                "duration": "23小时9分钟",
                "amount": "1.9115",
                "shells": "481.33",
            },
            {
                "date": "2024-05-05",
                "duration": "23小时56分钟",
                "amount": "1.9999",
                "shells": "475.72",
            },
            {
                "date": "2024-05-04",
                "duration": "23小时29分钟",
                "amount": "2.3442",
                "shells": "446.76",
            },
            {
                "date": "2024-05-03",
                "duration": "23小时56分钟",
                "amount": "1.6372",
                "shells": "401.31",
            },
            {
                "date": "2024-05-02",
                "duration": "23小时49分钟",
                "amount": "2.4318",
                "shells": "345.06",
            },
            {
                "date": "2024-05-01",
                "duration": "6小时14分钟",
                "amount": "0.6952",
                "shells": "77.90",
            },
        ],
    }
