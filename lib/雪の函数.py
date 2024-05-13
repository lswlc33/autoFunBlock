import os
import time
import datetime


def pTitle(str):
    title = f" {str} "
    terminal_width = os.get_terminal_size().columns
    title_length = sum(2 if is_chinese(ch) else 1 for ch in list(title))
    terminal_width -= int(title_length/2) + 2
    centered_title = title.center(terminal_width, "-")
    return centered_title


def is_chinese(char):
    if "\u4e00" <= char <= "\u9fff":
        return True
    else:
        return False


def cleanT():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def 当前时间():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def is_time_to_sleep():
    current_time = datetime.datetime.now().time()
    if current_time >= datetime.time(0, 0) and current_time <= datetime.time(8, 0):
        return True
    else:
        return False
