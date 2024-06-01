import os
from lib.宝石交易 import get_gift_logs

while 1:
    os.system("cls")
    choice = input("功能选择: 1.转赠记录 2.转赠宝石\n请选择: ")

    if choice == "1":
        while 1:
            os.system("cls")
            list = get_gift_logs().get("list", False)
            if list:
                for i in list:
                    rocks = float(i["rocks"])
                    print(
                        f"{i['datetime']} {i['rocks']} {'收到' if rocks > 0 else '赠送'} ID:{i['userId']} 昵称:{i['nickname']} "
                    )
            else:
                print("没有赠送记录")
            input("回车刷新...")
    elif choice == "2":
        os.system("cls")
        id = input("请输入要转赠的ID: ")
        num = input("请输入要转赠的数量: ")


        
        input("回车返回...")
