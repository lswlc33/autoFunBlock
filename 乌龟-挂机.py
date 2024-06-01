import threading, time
from lib.乌龟 import *
from lib.宝石矿洞 import *
from lib.登录信息 import *
from lib.贝壳 import 贝壳市场
from lib.账号 import 验证token
from lib.雪の函数 import cleanT, pTitle, is_time_to_sleep, 当前时间

data = ""
history = ""
乌龟ID = ""
is_sleep = 0
shell_sell_rice = 0


def pet_heartbeat():
    global is_sleep

    if not data:
        return
    # 睡眠检测
    if is_time_to_sleep():
        if data["desktopDisplay"] == 1:
            召回显示乌龟(0, 乌龟ID)
        is_sleep = 1
    else:
        if data["desktopDisplay"] == 0:
            召回显示乌龟(1, 乌龟ID)
        is_sleep = 0
    # 心跳
    try:
        if is_sleep:
            return
        宠物心跳()
    except Exception as e:
        print(f"\n刷新异常!\n{e}")
    heartbeat_thread = threading.Timer(5, pet_heartbeat)
    heartbeat_thread.start()


def update_data():
    """刷新数据"""
    global shell_sell_rice

    try:
        global data, history
        data = dict(获取乌龟信息())
        history = dict(捡宝历史())
        shell_sell_rice = float(贝壳市场(0)[0]["price"])

    except Exception as e:
        print("\n刷新异常!")
    update_thread = threading.Timer(2, update_data)
    update_thread.start()


def calc_shell_to_rock():
    return round(float(data["shells"]) * shell_sell_rice, 2)


def pick_up():
    """捡起宝石"""
    if is_sleep:
        return
    try:
        捡起宝石()
    except Exception as e:
        print(f"\n刷新异常!\n{e}")
    pickup_thread = threading.Timer(5, pick_up)
    pickup_thread.start()


def main():
    while True:
        try:
            cleanT()
            duration = (
                sum(
                    int(x) * 60**i
                    for i, x in enumerate(
                        reversed(
                            history["list"][0]["duration"]
                            .replace("小时", " ")
                            .replace("分钟", "")
                            .split()
                        )
                    )
                )
                / 60
            )
            时薪 = float(data["todayRocks"]) / duration if duration else 0
            print(
                f"\n 方块兽乌龟面板    时间: {当前时间(2)}",
                f"\n 乌龟自动喂养: {get_value('auto_feed')}   矿洞自动加时: {get_value('auto_extend')}",
                f"\n\n {pTitle('我的资产')}\n\n",
                f"{data['rocks']} 宝石    {data['shells']} 贝壳约 {calc_shell_to_rock()} 宝石",
                f"\n\n {pTitle(f'我的乌龟{{}}{{}}'.format('-睡眠中' if is_sleep else '','-捡宝中' if data['desktopDisplay'] else '-已召回'))}\n\n"
                f" 乌龟ID: {data['id']}\t   组件SN: {data['sn']}\n",
                f"乌龟性别：{data['gender']}\t代数: {data['generation']}\n",
                f"乌龟等级: {data['level']}\t进度: {data['levelProgress']}%\n",
                f"乌龟战力: {data['combatPower']}\n",
                f"耐力: {data['stamina']}  速度: {data['speed']}  力量: {data['strength']}  幸运: {data['luck']}\n",
                f"饥饿: {data['hunger']}   干净: {data['cleanliness']}   健康: {data['healthiness']}\n",
                f"探测器: {data['detector']}级",
                f"\n\n {pTitle(f'最新报告: {{}}'.format(history['list'][0]['date']))}\n\n",
                f"今日时长: {history['list'][0]['duration']}\n "
                f"今日预计: {round(时薪*16,3)} 宝石   时薪: {round(时薪,3)} 宝石\n "
                f"今日获取: {data['todayRocks']} 宝石   {data['todayShells']} 贝壳\n",
                f"\n {pTitle('开源项目')}\n\n",
                f"项目地址: github.com/lswlc33/autoFunBlock ",
            )
            if bool(get_value("auto_feed")) and not is_sleep:
                if int(data["hunger"]) < 78:
                    乌龟喂养(乌龟ID)
                    乌龟清理(乌龟ID)

            time.sleep(1)
        except Exception as e:
            if data != "":
                print(f"\n刷新异常!\n{e}")
            else:
                print("\n连接中...请等待！")
            time.sleep(1)


def cave_mine():
    try:
        挖矿(0)
        挖矿(1)
        if 剩余挖矿时间() < 24.00:
            挖矿(2)  # 自动加时
    except:
        pass
    cavemine_thread.start()


if __name__ == "__main__":
    # 检查登录信息
    cleanT()
    is_login = 验证token()
    if is_login.get("errorCode") == None:
        print(f"\n你好，{is_login['nickname']}!")
        time.sleep(1)
    else:
        print("\ntoken 验证失败，请重新登录!")
        input()
        exit()

    # 开始运行
    update_data()
    pet_heartbeat()
    pick_up()

    if get_value("auto_extend"):
        cavemine_thread = threading.Timer(300, cave_mine)
        cavemine_thread.start()

    main()
