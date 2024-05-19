import random
import pandas as pd
import math
from lib.大逃杀 import get_real_room, 大逃杀_信息

file_path = "data/escape.csv"


def read_csv():
    # 读取csv文件
    df = pd.read_csv(file_path)
    return df


def get_kill_room(场数, 房间ID):
    """
    获取指定房间在指定场次的击杀次数
    """
    df = read_csv()
    sorted_df = df.sort_values(by="期数", ascending=False)
    latest_df = sorted_df.head(场数)
    count = 0
    for i in latest_df["击杀房间"]:
        if i == 房间ID:
            count += 1
    return count


def get_room_rate(场数, 房间ID):
    """
    获取指定房间的击杀率
    :param 场数: 最近场数
    :param 房间ID: 房间编号
    :return: 击杀率
    """
    return get_kill_room(场数, 房间ID) / 场数


def get_f_rate(float):
    """
    将小数转换为百分数
    """
    return f"{math.floor(float * 1000) / 10}%"


def get_win_stat(num):
    """
    获取最近num场的胜率
    :param num: 最近场数
    :return: 胜场数，败场数，胜率
    """
    df = read_csv().sort_values(by="期数", ascending=False).head(num)
    win = 0
    lose = 0
    for i in df["是否获胜"]:
        if i == 1:
            win += 1
        elif i == -1:
            lose += 1
    if win == 0 and lose == 0:
        win_rate = "0%"
    else:
        win_rate = f"{round(win/(win + lose),3) * 100}%"
    return win, lose, win_rate


def get_m_stat(num):
    """
    获取最近num场的宝石统计
    :param num: 最近场数
    :return: 消耗宝石，获得宝石，盈亏
    """
    df = read_csv().tail(num)
    print(df)
    paid_m = round(sum(df["消耗宝石"]), 2)
    win_m = 0
    for i in range(len(df)):
        if df.iloc[i]["是否获胜"] != -1:
            win_m += df.iloc[i]["获得宝石"]
    win_m = round(win_m, 2)
    total_m = round(win_m - paid_m, 2)
    return paid_m, win_m, total_m


def get_best_room(type=1):
    """
    获取最佳房间
    """
    if type == 1:
        best_room = 0
        best_rate = 0
        for i in range(1, 9):
            rate = get_room_rate(1000, i)
            if rate > best_rate:
                best_rate = rate
                best_room = i
        return best_room
    elif type == 2:
        return random.randint(1, 8)
    elif type == 3:
        pass


if __name__ == "__main__":
    print(get_real_room(get_best_room()))