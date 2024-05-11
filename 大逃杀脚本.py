import csv
import os
import time
from lib.大逃杀 import 大逃杀_信息
from lib.雪の函数 import cleanT, pTitle, 当前时间


if __name__ == "__main__":
    data = ""
    当前期数 = 0
    if not os.path.exists("data/escape.csv"):
        with open("data/escape.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["期数","时间", "击杀房间", "上局击杀房间", "是否获胜", "消耗宝石", "获得宝石", "我的宝石"])


    while True:
        try:
            data = 大逃杀_信息()
            cleanT()
            print(
                f"\n {pTitle('大逃杀监控')}\n\n",
                f"当前期数: {data['issue']}\n",
                f"当前时间: {当前时间()}\n\n",
                f"{pTitle('本期信息')}\n\n",
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
                with open("data/escape.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            data["issue"],
                            当前时间(),
                            data["killNumber"],
                            data["prevRoomNumber"],
                            data["myIsWin"],
                            data["myCostMedal"],
                            data["myWinMedal"],
                            data["myWallet"],
                        ]
                    )
                当前期数 = data["issue"]
        except Exception as e:
            print(f"错误: {e}")
        time.sleep(1)

