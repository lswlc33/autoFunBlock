import requests
from lib.登录信息 import headers

session = requests.Session()


def 大逃杀_信息():
    response = session.post(
        url="https://block-api.lucklyworld.com/v11/api/room/escape/data",
        headers=headers,
    ).json()

    return {
        "issue": response["issue"],  # 期号
        "myWallet": response["myMedal"],  # 我的宝石
        "state": response["state"],  # 是否结算
        "killNumber": response["killNumber"],  # 击杀房间
        "prevRoomNumber": response["prevRoomNumber"],  # 上期击杀房间
        "countdown": response["countdown"],  # 倒计时
        "myWinMedal": response["myWinMedal"],  # 获得宝石
        "myIsWin": response["myIsWin"],  # 是否获胜
        "myCostMedal": response["myCostMedal"],  # 消耗宝石
    }


def 大逃杀_投入(roomNumber, costMedal):
    """
    :param roomNumber: 房间号
    :param costMedal: 投入宝石 0.1 1 10 50 100
    """
    response = session.post(
        url="https://block-api.lucklyworld.com/v11/api/room/escape/buy",
        data=f"roomNumber={roomNumber}&costMedal={costMedal}",
        headers=headers,
    ).json()

    return response


def get_real_room(num):
    rooms = [
        "杂物间",
        "休息室",
        "厂长室",
        "谈话室",
        "洗衣房",
        "工作室",
        "茶水间",
        "音乐室",
    ]
    return rooms[int(num) - 1]
