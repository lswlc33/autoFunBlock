import time,os
from lib.大逃杀 import get_real_room,大逃杀_信息,大逃杀_投入
from lib.雪の函数 import 当前时间
from lib.大逃杀计算 import get_best_room

os.system('clear')

is_paid = 0
is_upated = 0
count = 0.1
issue = 大逃杀_信息()["issue"]
while True:
    try:
        new_issue = 大逃杀_信息()["issue"]
        if not is_upated and new_issue != issue:
            print(f"{当前时间()}  进入第 {new_issue} 期")
            issue = new_issue
            is_paid = 0
            is_upated = 1
        
        if 5 < 大逃杀_信息()["countdown"] < 40 and not is_paid:
            roomid = get_best_room()
            大逃杀_投入(roomNumber=roomid,costMedal=count)
            print(f"{当前时间()}  投入 {get_real_room(roomid)} 一次宝石 {count}")

            is_paid = 1
            is_upated = 0

    
    except Exception as e:
        print(e)
    time.sleep(3)