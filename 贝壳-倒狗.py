from lib.贝壳 import 贝壳信息, 贝壳市场, 贝壳交易
from lib.雪の函数 import 当前时间


myshell = 0
myrock = 0
last_price1 = 0
last_price2 = 0
last_sell_price = 999999999999  # 防止高买低卖
stay_time = 0  # 系统日志停留时间
is_working = 0  # 防止无辜输出被覆盖


# 有交易成功操作记录日志
def write_log(time, type, price, all):
    with open("data/shell.log", "a+") as f:
        f.write(f"{time}, {type}, {price}, {all}\n")


def 倒狗启动():
    global last_sell_price, last_price1, last_price2, myshell, myrock, stay_time, is_working

    try:
        # 获取市场信息
        index = 贝壳信息()
        myshell = round(float(index["shells"]))
        myrock = round(float(index["rocks"]), 2)
        data1 = 贝壳市场(0)[0]
        data2 = 贝壳市场(1)[0]
        tradeId1, quantity1, price1, tradeId2, quantity2, price2 = (
            float(data1["tradeId"]),
            float(data1["quantity"]),
            float(data1["price"]),
            float(data2["tradeId"]),
            float(data2["quantity"]),
            float(data2["price"]),
        )

        # 判断价格是否更新
        if price1 != last_price1 or price2 != last_price2 or is_working != 0:
            print(
                f"[ {'🤩' if price2 < price1 else '0'} ]\t宝石: {round(myrock,2)}  贝壳: {round(myshell,0)}  求购价:{price1} \t出售价:{price2}",
            )
            last_price1, last_price2 = price1, price2
            stay_time = 0
            is_working = 0
        else:
            stay_time += 1
            print(
                f"\033[1A\r\033[K[ {'🤩' if price2 < price1 else stay_time} ]\t宝石: {round(myrock,2)}  贝壳: {round(myshell,0)}  求购价:{price1} \t出售价:{price2}"
            )
            return

        # 秒杀高价求购
        if price1 >= 0.01:
            is_working = 1
            need_to_sell = min(quantity1, myshell)
            r = 贝壳交易(1, tradeId1, need_to_sell)
            if r["message"] == "OK":
                print(
                    f"\033[31m秒杀高价求购贝壳 {need_to_sell} 获得 {need_to_sell*price1} 宝石\033[39m"
                )
                write_log(当前时间(), "++", price1, need_to_sell * price1)
            elif r["message"] == "":
                print(f"错误: 未知错误")
            else:
                print(f'错误: {r["message"]}')
            return

        # 秒杀低价出售
        if price2 <= 0.001:
            is_working = 1
            r = 贝壳交易(0, tradeId2, quantity2)
            if r["message"] == "OK":
                print(
                    f"\033[31m秒杀低价出售贝壳 {quantity2} 花费 {quantity2*price2} 宝石\033[39m"
                )
                write_log(当前时间(), "--", price2, quantity2 * price2)
            elif r["message"] == "":
                print(f"错误: 未知错误")
            else:
                print(f'错误: {r["message"]}')
            return

        # 出掉多余的宝石
        if myshell > 210 and last_sell_price <= price1:
            is_working = 1
            quantity1 = quantity1 if quantity1 <= 10 else quantity1 - 10
            need_to_sell = min(quantity1, myshell - 200)
            r = 贝壳交易(1, tradeId1, need_to_sell)
            if r["message"] == "OK":
                print(
                    f"\033[31m清理库存贝壳 {need_to_sell} 获得 {need_to_sell*price1} 宝石\033[39m"
                )
                write_log(当前时间(), "+", price1, need_to_sell * price1)
                last_sell_price = 999999999999
            elif r["message"] == "":
                print(f"错误: 未知错误")
            else:
                print(f'错误: {r["message"]}')
            return

        # 开导
        if price2 < price1:
            is_working = 1
            quantity = min(quantity1, quantity2)
            r = 贝壳交易(0, tradeId2, quantity)
            if r["message"] == "OK":
                print(f"\033[31m购入贝壳 {quantity} 花费 {quantity*price2}\033[39m")
                write_log(当前时间(), "-", price2, quantity * price2)
                r = 贝壳交易(1, tradeId1, quantity)
                if r["message"] == "OK":
                    print(f"\033[31m售出贝壳 {quantity} 获得 {quantity*price1}\033[39m")
                    write_log(当前时间(), "+", price1, quantity * price1)
                elif r["message"] == "":
                    print(f"错误: 未知错误")
                    last_sell_price = price2
                else:
                    print(f'错误: {r["message"]}')
                    last_sell_price = price2
            elif r["message"] == "":
                print(f"错误: 未知错误")
            else:
                print(f'错误: {r["message"]}')

            return
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    print("\033c\033[?25l\n    开始运行 ...\n")
    while 1:
        倒狗启动()
