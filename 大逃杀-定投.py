import random
import time
from lib.大逃杀 import get_real_room, 大逃杀_信息, 大逃杀_投入
from lib.雪の函数 import 当前时间, cleanT

cleanT()

is_paid = 0
is_upated = 0
roomid = 0
win_m = 0
issue = 大逃杀_信息()["issue"]
投入宝石 = input("输入投入定投宝石: ")
print("1. 固定房间")
print("2. 随机房间")
print("3. 加一模式")
定投模式 = input("输入定投模式(1-3): ")
if 定投模式 == "1":
    roomid = input("输入房间号(1-8): ")


cleanT()
print(f"{当前时间()} 开始")

while True:
    try:
        issue_info = 大逃杀_信息()
        new_issue, prevRoomNumber = issue_info["issue"], issue_info["prevRoomNumber"]
        if issue_info["myWinMedal"] != "0":
            win_m = float(issue_info["myWinMedal"])

        if not is_upated and new_issue != issue:
            if is_paid:
                # 判断上局胜负
                red = "\033[31m凉了\033[39m"
                if int(roomid) == int(prevRoomNumber):
                    print(f"{当前时间()}  第 {new_issue-1} 期 {red}")
                else:
                    print(
                        f"{当前时间()}  第 {new_issue-1} 期 赢了 获得 {win_m-投入宝石} 宝石"
                    )
            print(f"{当前时间()}  进入第 {new_issue} 期")
            issue = new_issue
            is_paid = 0
            is_upated = 1

        # 倒计时 40 秒后投入
        if 5 < 大逃杀_信息()["countdown"] < 40 and not is_paid:
            if 定投模式 == "1":
                大逃杀_投入(roomNumber=roomid, costMedal=投入宝石)
            elif 定投模式 == "2":
                roomid = random.randint(1, 8)
                大逃杀_投入(roomNumber=roomid, costMedal=投入宝石)
            elif 定投模式 == "3":
                roomid = (int(prevRoomNumber) + 1) if int(prevRoomNumber) <= 7 else 1
                大逃杀_投入(roomNumber=roomid, costMedal=投入宝石)
            print(f"{当前时间()}  投入 {get_real_room(roomid)} 宝石 {投入宝石}")

            is_paid = 1
            is_upated = 0

    except Exception as e:
        print(e)
    time.sleep(3)
