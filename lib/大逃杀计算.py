import pandas as pd
import math
from lib.大逃杀 import get_real_room, 大逃杀_信息


def read_csv(file_path):
    # 读取csv文件
    df = pd.read_csv(file_path)
    return df


def get_kill_room(场数, 房间ID):
    df = read_csv("data/escape.csv")
    sorted_df = df.sort_values(by="期数", ascending=False)
    latest_df = sorted_df.head(场数)
    count = 0
    for i in latest_df["击杀房间"]:
        if i == 房间ID:
            count += 1
    return count


def get_room_rate(场数, 房间ID):
    return get_kill_room(场数, 房间ID) / 场数


def get_f_rate(float):
    return f"{math.floor(float * 1000) / 10}%"


def get_best_room(type=1):
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
        pass


if __name__ == "__main__":
    print(get_real_room(get_best_room()))
