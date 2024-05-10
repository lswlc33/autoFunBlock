import threading, os, time
from 乌龟 import *
from 宝石矿洞 import *
from 登录信息 import *
from 账号 import 验证token

data = ""
history = ""
乌龟ID = ""


def cleanT():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pet_heartbeat():
    while True:
        try:
            宠物心跳()
            time.sleep(1)
        except Exception as e:
            print("\n刷新异常!")
            time.sleep(1)


def update_data():
    while True:
        try:
            global data, history
            data = dict(获取乌龟信息())
            history = dict(捡宝历史())
            time.sleep(1)
        except Exception as e:
            print("\n刷新异常!")
            time.sleep(1)


def pick_up():
    while True:
        try:
            捡起宝石()
        except Exception as e:
            print("\n刷新异常!")
            time.sleep(60)


def main():
    while True:
        try:
            cleanT()
            print(
                f"\n 方块兽乌龟面板    时间: {time.strftime('%m-%d %H:%M:%S')}",
                f"\n 乌龟自动喂养: {get_value('auto_feed')}   矿洞自动加时: {get_value('auto_extend')}",
                f"\n\n {'-' * 40}\n\n",
                f"乌龟ID: {data['id']}\t   组件SN: {data['sn']}\n",
                f"{data['rocks']} 宝石\t   {data['shells']}贝壳",
                f"\n\n {'-' * 40}\n\n",
                f"乌龟性别：{data['gender']}\t代数: {data['generation']}\n",
                f"乌龟等级: {data['level']}\t进度: {data['levelProgress']}%\n",
                f"乌龟战力: {data['combatPower']}\n",
                f"耐力: {data['stamina']}  速度: {data['speed']}  力量: {data['strength']}  幸运: {data['luck']}\n",
                f"饥饿: {data['hunger']}   干净: {data['cleanliness']}   健康: {data['healthiness']}\n",
                f"探测器: {data['detector']}级",
                f"\n\n {'-' * 40}\n\n",
                f"今日时长: {history['list'][0]['duration']}\n "
                f"今日获取: {data['todayRocks']} 宝石   {data['todayShells']}贝壳\n",
            )
            if bool(get_value("auto_feed")):
                if int(data["hunger"]) < 80:
                    乌龟喂养(乌龟ID)
                    乌龟清理(乌龟ID)

            time.sleep(1)
        except Exception as e:
            if data != "":
                print("\n刷新异常!")
            else:
                print("\n连接中...请等待！")
            time.sleep(1)


def cave_mine():
    while True:
        try:
            挖矿(0)
            挖矿(1)
            if 剩余挖矿时间() < 24.00:
                挖矿(2)  # 自动加时
        except:
            pass
        time.sleep(600)


if __name__ == "__main__":
    # 检查登录信息
    cleanT()
    is_login = 验证token()
    if is_login.get("errorCode") == None:
        print(f"\n你好，{is_login['nickname']}!")
        time.sleep(1)
    else:
        print("\ntoken 验证失败，请重新登录!")
        exit()
        input()

    # 开始挂
    update_thread = threading.Thread(target=update_data)
    update_thread.start()

    heartbeat_thread = threading.Thread(target=pet_heartbeat)
    heartbeat_thread.start()

    pickup_thread = threading.Thread(target=pick_up)
    pickup_thread.start()

    if get_value("auto_extend"):
        cavemine_thread = threading.Thread(target=cave_mine)
        cavemine_thread.start()

    main()
