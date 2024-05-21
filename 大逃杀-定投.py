import random
import time
from lib.大逃杀 import get_real_room, 大逃杀_信息, 大逃杀_投入
from lib.雪の函数 import decompose_number, 当前时间, cleanT

概率宝石 = ""
宝石模式 = 0
定投模式 = 0

is_paid = 0
is_updated = 0
roomid = 0
rock_num = 0
win_m = 0
issue = 0
prevRoomNumber = 0


def 信息询问():
    global 宝石模式, rock_num, 概率宝石, 定投模式, roomid
    print("信息配置")
    print("1. 固定宝石")
    print("2. 概率宝石(多个数,英文逗号分隔)")
    print("例: 0.1, 0.1, 0.2, 0.2, 0.2 为 40% 0.1 60% 0.2")
    宝石模式 = input("输入宝石模式(1-2): ")
    if 宝石模式 == "1":
        rock_num = input("输入投入定投宝石: ")
    elif 宝石模式 == "2":
        概率宝石 = input("请按照例子书写概率：").split(",")

    print("1. 固定房间")
    print("2. 随机房间")
    print("3. 加一模式")
    定投模式 = input("输入定投模式(1-3): ")
    if 定投模式 == "1":
        roomid = input("输入房间号(1-8): ")


def 投入宝石():
    global rock_num
    if 宝石模式 == "1":
        pass
    elif 宝石模式 == "2":
        rock_num = random.choice(概率宝石).strip()


def 投入房间():
    global roomid
    if 定投模式 == "1":
        pass
    elif 定投模式 == "2":
        roomid = random.randint(1, 8)
    elif 定投模式 == "3":
        roomid = (int(prevRoomNumber) + 1) if int(prevRoomNumber) <= 7 else 1


def 投入(rock_num):
    r = 大逃杀_投入(roomNumber=roomid, costMedal=rock_num)
    if r.get("message", "ok") == "ok":
        print(f"{当前时间()}  投入 {get_real_room(roomid)} 宝石 {rock_num}")
    else:
        print(f"{当前时间()}  投入失败 {r.get('message', 'ok')}")


def main():
    global is_paid, is_updated, roomid, rock_num, win_m, issue, prevRoomNumber
    try:
        issue_info = 大逃杀_信息()
        new_issue, prevRoomNumber = issue_info["issue"], issue_info["prevRoomNumber"]
        if issue_info["myWinMedal"] != "0":
            win_m = float(issue_info["myWinMedal"])

        if not is_updated and new_issue != issue:
            if is_paid:
                # 判断上局胜负
                red = "\033[31m凉了TAT\033[39m"
                if int(roomid) == int(prevRoomNumber):
                    print(f"{当前时间()}  第 {new_issue-1} 期 {red}")
                else:
                    win_m_num = round(win_m-float(rock_num),4) if win_m else "不知道"
                    print(
                        f"{当前时间()}  第 {new_issue-1} 期 赢得 {win_m_num} 宝石"
                    )
            print(f"{当前时间()}  进入第 {new_issue} 期")
            issue = new_issue
            is_paid = 0
            is_updated = 1

        # 倒计时 40 秒后投入
        if 5 < 大逃杀_信息()["countdown"] < 40 and not is_paid:
            投入宝石()
            投入房间()

            for i in decompose_number(rock_num):
                投入(i)

            is_paid = 1
            is_updated = 0

    except Exception as e:
        print(e)
    time.sleep(3)


if __name__ == "__main__":
    cleanT()
    信息询问()
    cleanT()

    print(f"{当前时间()} 开始")

    while 1:
        main()
