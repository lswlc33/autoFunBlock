import os
import datetime


def pTitle(str):
    title = f" {str} "
    terminal_width = os.get_terminal_size().columns
    title_length = sum(2 if is_chinese(ch) else 1 for ch in list(title))
    terminal_width -= int(title_length / 2) + 2
    centered_title = title.center(terminal_width, "-")
    return centered_title


def is_chinese(char):
    if "\u4e00" <= char <= "\u9fff":
        return True
    else:
        return False


def cleanT():
    os.system("cls" if os.name == "nt" else "clear")


def 当前时间(type=1):
    now_time = datetime.datetime.now()
    if type == 1:
        return now_time.strftime("%Y-%m-%d %H:%M:%S")
    if type == 2:
        return now_time.strftime("%m月%d %H:%M:%S")


def is_time_to_sleep():
    current_time = datetime.datetime.now().time()
    return datetime.time(0, 0) <= current_time <= datetime.time(8, 0)


def decompose_number(num):
    result = []
    num = str(num)
    in1, flo = num.split(".")
    in1 = int(in1)
    flo = float(f"0.{flo}")
    while in1 > 0:
        if in1 >= 100:
            result.append(100)
            in1 -= 100
        elif in1 >= 50:
            result.append(50)
            in1 -= 50
        elif in1 >= 10:
            result.append(10)
            in1 -= 10
        elif in1 >= 1:
            result.append(1)
            in1 -= 1
    while flo > 0:
        if flo >= 0.1:
            result.append(0.1)
            flo = round(flo - 0.1, 1)

    return result
