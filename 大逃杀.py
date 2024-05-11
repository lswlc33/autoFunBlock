import requests, time, os
import csv
from 登录信息 import headers

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

    print(response)


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
    return rooms[num - 1]


if __name__ == "__main__":
    data = ""
    当前期数 = 0
    while True:
        data = 大逃杀_信息()
        os.system("cls")
        print(
            f"当前期数: {data['issue']}\n",
            f"倒计时: {data['countdown']}\n",
            f"是否结算: {data['state']}\n",
            f"击杀房间: {data['killNumber']}\n",
            f"上期击杀房间: {data['prevRoomNumber']}\n",
            f"是否获胜: {data['myIsWin']}\n",
            f"消耗宝石: {data['myCostMedal']}\n",
            f"获得宝石: {data['myWinMedal']}\n",
            f"我的宝石: {data['myWallet']}\n",
        )

        if data["state"] == 2 and 当前期数 != data["issue"]:
            with open("escape.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        data["issue"],
                        data["killNumber"],
                        data["prevRoomNumber"],
                        data["myIsWin"],
                        data["myCostMedal"],
                        data["myWinMedal"],
                        data["myWallet"],
                    ]
                )
            当前期数 = data["issue"]

        time.sleep(1)