from concurrent.futures import thread
import time
from lib.贝壳 import 贝壳信息, 贝壳市场, 贝壳交易
from lib.雪の函数 import 当前时间
import threading


shells_info = {
    "myshells": None,
    "myrocks": None,
    "tradeId1": None,
    "quantity1": None,
    "price1": None,
    "tradeId2": None,
    "quantity2": None,
    "price2": None,
}

def update_wallet_info():
    """钱包"""
    global shells_info
    index = 贝壳信息()
    shells_info["myshells"] = round(float(index["shells"]))
    shells_info["myrocks"] = round(float(index["rocks"]), 2)
    wallet_info_timer = threading.Timer(0.5, update_wallet_info)
    wallet_info_timer.start()

def update_market_info():
    """更新市场信息"""
    global shells_info

    data1 = 贝壳市场(0)[0]
    data2 = 贝壳市场(1)[0]

    if shells_info["tradeId1"] != int(data1["tradeId"]) or shells_info["tradeId2"] != int(data2["tradeId"]):
        shells_info["price1"] = float(data1["price"])
        shells_info["price2"] = float(data2["price"])
        shells_info["quantity1"] = int(data1["quantity"])
        shells_info["quantity2"] = int(data2["quantity"])
        print(
            shells_info["myrocks"],shells_info["myshells"] ,
            shells_info["price1"], shells_info["price2"],
            shells_info["quantity1"], shells_info["quantity2"])


    shells_info["tradeId1"] = int(data1["tradeId"])
    shells_info["tradeId2"] = int(data2["tradeId"])




def buy_shell(id, quantity):
    """购买"""
    r = 贝壳交易(0, id, quantity)
    if r.get("errorCode"):
        print(f"购买失败: {r.get("message")}")
        return False
    else:
        print("购买成功")
        return True

def sell_shell(id, quantity):
    """出售"""
    r = 贝壳交易(1, id, quantity)
    if r.get("errorCode"):
        print(f"出售失败: {r.get("message")}")
        return False
    else:
        print("出售成功")
        return True


def check_market_loop():
    if shells_info["myshells"] >= 300.00:
        quantity = min(200,shells_info["myshells"] - 201)
        sell_shell(shells_info["tradeId1"] - 10, quantity)

    if shells_info["price1"] >= 0.01:
        quantity = min(shells_info["quantity1"],shells_info["myshells"] - 201)
        sell_shell(shells_info["tradeId1"], quantity)

    elif shells_info["price2"] < 0.001:
        buy_shell(shells_info["tradeId2"], shells_info["quantity2"])

    elif shells_info["price1"] > shells_info["price2"]:
        quantity = min(1000, shells_info["quantity1"], shells_info["quantity2"])

        if buy_shell(shells_info["tradeId2"], quantity):
            sell_shell(shells_info["tradeId1"], quantity)
        time.sleep(1)

print("\033c\033[?25l", end="")

wallet_info_timer = threading.Timer(0, update_wallet_info)
wallet_info_timer.start()

while True:
    update_market_info()
    time.sleep(0.5)
    check_market_loop()
