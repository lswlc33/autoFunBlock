import time
from lib.雪の函数 import cleanT
from lib.虎口逃生 import (
    escape_participate,
    escape_polling,
    escape_run_list,
    escape_placing,
)

info = {
    "animalId": None,
    "itemId": None,
    "itemNum": None,
    "type": None,
    "is_participate": False,
    "is_placing": False,
    "is_get_result": False,
    "is_reset": False,
    "result": None,
    "win": 0,
    "lose": 0,
    "profit": 0,
}


def get_escapeResult():
    """
    return:
    myState: 输赢状态
    animalId: 投入的动物
    killedAnimalId: 击杀的动物
    myInputGem: 投入宝石
    getGem: 获得宝石
    """
    data = escape_run_list()
    if data["ok"]:
        return data["escapeResult"]
    return False


def reset_escape():
    if info["is_reset"]:
        return
    info["is_participate"] = False
    info["is_placing"] = False
    info["is_reset"] = True


def main():
    global info
    data = escape_polling()
    cleanT()
    print(f"倒计时: {data['countdown']}")
    print("-" * 20)
    print(f"期数: {data['issue']} 宝石: {data['myGem']}")
    print(f"赢: {info['win']} 输: {info['lose']} 利润: {info['profit']}")
    print(
        "已参与:",
        info["is_participate"],
        "已投入:",
        info["is_placing"],
        "已结算:",
        info["is_get_result"],
    )
    print("-" * 20)
    if info["result"]:
        print(f"输赢: {info['result']['myState']}")
        print(
            f"投入动物: {info['result']['animalId']}, 击杀动物: {info['result']['killedAnimalId']}"
        )
        print(
            f"投入宝石: {info['result']['myInputGem']}, 获得宝石: {info['result']['getGem']}"
        )
    else:
        print("等待结算")
    print("-" * 20)
    if data["status"] == 0:
        print("😴 未开始")
        reset_escape()

    if data["status"] == 1:
        print("🥰 进行中")
        if info["is_get_result"]:
            info["is_get_result"] = False
        if not info["is_participate"]:
            escape_participate(info["animalId"])
            info["is_participate"] = True
            info["is_reset"] = False
        if not info["is_placing"]:
            escape_placing(info["itemId"], info["itemNum"])
            info["is_placing"] = True

    if data["status"] == 2:
        print("🏆 已结束")
        if info["is_get_result"]:
            return
        res = get_escapeResult()

        if res:
            info["is_get_result"] = True
            info["result"] = res
            if res["myState"] == 1:
                info["win"] += 1
            else:
                info["lose"] += 1
            info["profit"] += round(float(res["getGem"]) - float(res["myInputGem"]), 4)
            reset_escape()

    time.sleep(2)


if __name__ == "__main__":
    cleanT()
    print("选择投入的动物:")
    print("1.🐶 狗子  2.🐗 野猪  3.🦊 狐狸 ")
    print("4.🦍 巨猿  5.🦝 浣熊  6.🐂 牛牛")
    info["animalId"] = input("请输入编号: ")

    cleanT()
    print("选择投入的道具:")
    print("1. 香蕉皮(0.1) 2.树枝(0.5) 3.泥潭(1.0)")
    print("11.护盾(0.5)  12.加速(0.5)")
    info["itemId"] = input("请输入编号: ")

    cleanT()
    print("选择投入道具的数量:")
    info["itemNum"] = input("请输入数量: ")

    cleanT()
    print("选择投入方式:")
    print("1.固定动物与道具")
    info["type"] = input("请输入编号: ")

    while 1:
        try:
            main()
        except:
            print("出错了")
            time.sleep(1)
            continue
