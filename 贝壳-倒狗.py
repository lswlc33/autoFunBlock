import time
from lib.贝壳 import 贝壳信息, 贝壳市场, 贝壳交易
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
    "is_sold": True,
    "sold_quantity": 0,
}


def update_wallet_info():
    """钱包"""
    global shells_info
    try:
        index = 贝壳信息()
        shells_info["myshells"] = round(float(index["shells"]))
        shells_info["myrocks"] = round(float(index["rocks"]), 2)
    except Exception as e:
        pass
    wallet_info_timer = threading.Timer(1, update_wallet_info)
    wallet_info_timer.start()


def update_market_info():
    """更新市场信息"""
    global shells_info

    data1 = 贝壳市场(0)[0]
    data2 = 贝壳市场(1)[0]

    if shells_info["tradeId1"] != int(data1["tradeId"]) or shells_info[
        "tradeId2"
    ] != int(data2["tradeId"]):
        shells_info["price1"] = float(data1["price"])
        shells_info["price2"] = float(data2["price"])
        shells_info["quantity1"] = int(data1["quantity"])
        shells_info["quantity2"] = int(data2["quantity"])
        print(
            shells_info["myrocks"],
            shells_info["myshells"],
            shells_info["price1"],
            shells_info["price2"],
            shells_info["quantity1"],
            shells_info["quantity2"],
        )

    shells_info["tradeId1"] = int(data1["tradeId"])
    shells_info["tradeId2"] = int(data2["tradeId"])


def buy_shell(id, quantity):
    """购买"""
    r = 贝壳交易(0, id, quantity)
    if r.get("errorCode"):
        print(f"购买失败: {r.get('message')}")
        return False
    else:
        print("购买成功")
        return True


def sell_shell(id, quantity):
    """出售"""
    r = 贝壳交易(1, id, quantity)
    if r.get("errorCode"):
        print(f"出售失败: {r.get('message')}")
        return False
    else:
        print("出售成功")
        return True


def check_market_loop():
    global shells_info

    if not shells_info["is_sold"]:
        if shells_info["myshells"] < 200.0:
            shells_info["is_sold"] = True
        print("补救流程")
        if shells_info["sold_quantity"] > shells_info["quantity1"]:
            if sell_shell(shells_info["tradeId1"], shells_info["quantity1"]):
                shells_info["sold_quantity"] = (
                    shells_info["sold_quantity"] - shells_info["quantity1"]
                )
        else:
            shells_info["is_sold"] = sell_shell(
                shells_info["tradeId1"], shells_info["sold_quantity"]
            )

    elif shells_info["myshells"] >= 300.00:
        print("闲置流程")
        quantity = min(200, shells_info["myshells"] - 201)
        sell_shell(shells_info["tradeId1"], quantity - 10)

    elif shells_info["price1"] >= 0.01:
        print("高价流程")
        quantity = min(shells_info["quantity1"], shells_info["myshells"] - 201)
        sell_shell(shells_info["tradeId1"], quantity)

    elif shells_info["price2"] < 0.001:
        print("低价流程")
        buy_shell(shells_info["tradeId2"], shells_info["quantity2"])

    elif shells_info["price1"] > shells_info["price2"]:
        print("交换流程")
        quantity = min(1000, shells_info["quantity1"], shells_info["quantity2"])
        if buy_shell(shells_info["tradeId2"], quantity):
            shells_info["is_sold"] = sell_shell(shells_info["tradeId1"], quantity)
            shells_info["sold_quantity"] = quantity
        time.sleep(1)


print("\033c\033[?25l", end="")

update_wallet_info()

while True:
    try:
        update_market_info()
        time.sleep(0.5)
        check_market_loop()
    except KeyError:
        pass
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
