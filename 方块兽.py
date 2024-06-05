import base64
import csv
import tkinter as tk
from tkinter import messagebox, ttk
import threading, time
from lib.乌龟 import *
from lib.大逃杀 import get_real_room, 大逃杀_信息
from lib.大逃杀计算 import get_m_stat, get_win_stat
from lib.宝石交易 import get_gift_logs
from lib.宝石矿洞 import *
from lib.登录信息 import *
from lib.贝壳 import 贝壳市场
from lib.账号 import 发送验证码, 登录, 验证token
import res.favicon as favicon
from lib.雪の函数 import is_time_to_sleep, 当前时间


data = ""
history = ""
乌龟ID = ""
is_sleep = 0
shell_sell_rice = 0
need_stop = 0


def send_code():
    res = 发送验证码(login_entry_phone.get())
    print(res)
    if res.get("errorCode") == 400:
        messagebox.showerror("错误", f"发送失败! {res.get('message')}")
    else:
        messagebox.showinfo("成功", "发送成功")


def login():
    res = 登录(login_entry_phone.get(), login_entry_code.get())
    if res.get("errorCode") == 400:
        messagebox.showerror(f"登录失败! ", "{res.get('message')}")
    else:
        messagebox.showinfo("登录成功!", "token 已经写入 setting.ini")
        write_value("token", res.get("token"))
        login_text_token.insert(1.0, res.get("token"))


def get_login():
    time.sleep(1)
    is_login = 验证token()
    if is_login.get("errorCode") == None:
        app.title(f"{is_login['nickname']} - 方块兽")
        # 开始运行
        threading.Thread(target=update_data).start()
        threading.Thread(target=main).start()
        threading.Thread(target=pet_heartbeat).start()
        threading.Thread(target=pick_up).start()
        if get_value("auto_extend"):
            cave_mine()
    else:
        app.title(f"未登录或登录过期 - 方块兽")


def escape_watch_loop():
    data = ""
    当前期数 = 0
    num = 2000
    if not os.path.exists("data/escape.csv"):
        with open("data/escape.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "期数",
                    "时间",
                    "击杀房间",
                    "上局击杀房间",
                    "是否获胜",
                    "消耗宝石",
                    "获得宝石",
                    "我的宝石",
                ]
            )

    while True:
        try:
            if need_stop:
                return
            data = 大逃杀_信息()
            win, lose, win_rate = get_win_stat(num)
            paid_m, win_m, total_m = get_m_stat(num)

            escape_wacth_textarea_text.set(
                f"\n⨀ {'大逃杀监控'}\n\n"
                + f" 当前期数: {data['issue']}\n"
                + f" 当前时间: {当前时间()}\n\n"
                + f"⨀ 本期信息\n\n"
                + f" 倒计时: {data['countdown']}\t\t是否获胜: {data['myIsWin']}\n"
                + f" 本期击杀: {get_real_room(data['killNumber'])}\t上期击杀: {get_real_room(data['prevRoomNumber'])}\n"
                + f" 是否结算: {'是' if data['state']==2 else '否'}\t\t我的宝石: {data['myWallet']}\n"
                + f"\n⨀ {f'近 {num} 场数据胜率'}\n\n"
                + f" 胜场: {win}\t败场: {lose}\t胜率: {win_rate}\n"
                + f" 投入: {paid_m}\t赚的: {win_m}\t利润: {total_m}"
            )

            if data["state"] == 2 and 当前期数 != data["issue"]:
                with open("data/escape.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            data["issue"],
                            当前时间(),
                            data["killNumber"],
                            data["prevRoomNumber"],
                            data["myIsWin"],
                            data["myCostMedal"],
                            data["myWinMedal"],
                            data["myWallet"],
                        ]
                    )
                当前期数 = data["issue"]
        except Exception as e:
            print(f"错误: {e}")
        time.sleep(1)


def start_escape_wacth():
    threading.Thread(target=escape_watch_loop).start()
    escape_button_start.place_forget()


def pet_heartbeat():
    global is_sleep
    if need_stop:
        return
    try:
        if not data:
            raise Exception("获取失败")
        # 睡眠检测
        if is_time_to_sleep():
            if data["desktopDisplay"] == 1:
                召回显示乌龟(0, 乌龟ID)
            is_sleep = 1
        else:
            if data["desktopDisplay"] == 0:
                召回显示乌龟(1, 乌龟ID)
            is_sleep = 0
        # 心跳
        if not is_sleep:
            宠物心跳()
    except Exception as e:
        print(f"\n刷新异常!\n{e}")
    heartbeat_thread = threading.Timer(5, pet_heartbeat)
    heartbeat_thread.start()


def update_data():
    """刷新数据"""
    global shell_sell_rice
    if need_stop:
        return
    try:
        global data, history
        data = dict(获取乌龟信息())
        history = dict(捡宝历史())
        shell_sell_rice = float(贝壳市场(0)[0]["price"])
    except KeyError:
        pass
    except Exception as e:
        print(f"\n刷新异常!\n{e}")
    update_thread = threading.Timer(2, update_data)
    update_thread.start()


def calc_shell_to_rock():
    return round(float(data["shells"]) * shell_sell_rice, 2)


def pick_up():
    """捡起宝石"""
    if need_stop:
        return
    if is_sleep:
        return
    try:
        捡起宝石()
    except Exception as e:
        print(f"\n刷新异常!\n{e}")
    pickup_thread = threading.Timer(5, pick_up)
    pickup_thread.start()


def main():
    while True:
        if need_stop:
            return
        try:
            duration = (
                sum(
                    int(x) * 60**i
                    for i, x in enumerate(
                        reversed(
                            history["list"][0]["duration"]
                            .replace("小时", " ")
                            .replace("分钟", "")
                            .split()
                        )
                    )
                )
                / 60
            )
            时薪 = float(data["todayRocks"]) / duration if duration else 0
            pet_info_text.set(
                f"\n 方块兽乌龟面板    时间: {当前时间(2)}\n"
                + f" 乌龟自动喂养: {get_value('auto_feed')}   矿洞自动加时: {get_value('auto_extend')}\n"
                + f"\n⨀ 我的资产\n\n"
                + f" {data['rocks']} 宝石    {data['shells']} 贝壳约 {calc_shell_to_rock()} 宝石\n"
                + f"\n⨀ {f'我的乌龟{{}}{{}}'.format('-睡眠中' if is_sleep else '','-捡宝中' if data['desktopDisplay'] else '-已召回')}\n\n"
                + f" 乌龟ID: {data['id']}\t   组件SN: {data['sn']}\n"
                + f" 乌龟性别：{data['gender']}\t代数: {data['generation']}\n"
                + f" 乌龟等级: {data['level']}\t进度: {data['levelProgress']}%\n"
                + f" 乌龟战力: {data['combatPower']}\n"
                + f" 耐力: {data['stamina']}  速度: {data['speed']}  力量: {data['strength']}  幸运: {data['luck']}\n"
                + f" 饥饿: {data['hunger']}   干净: {data['cleanliness']}   健康: {data['healthiness']}\n"
                + f" 探测器: {data['detector']}级\n"
                + f"\n⨀ {f'最新报告: {{}}'.format(history['list'][0]['date'])}\n\n"
                + f" 今日时长: {history['list'][0]['duration']}\n"
                + f" 今日预计: {round(时薪*16,3)} 宝石   时薪: {round(时薪,3)} 宝石\n"
                + f" 今日获取: {data['todayRocks']} 宝石   {data['todayShells']} 贝壳\n"
                + f"\n⨀ 开源项目\n\n"
                + f" 项目地址: github.com/lswlc33/autoFunBlock"
            )

            if bool(get_value("auto_feed")) and not is_sleep:
                if int(data["hunger"]) < 78:
                    乌龟喂养(乌龟ID)
                    乌龟清理(乌龟ID)

            time.sleep(1)
        except Exception as e:
            if data != "":
                print(f"\n刷新异常!\n{e}")
            else:
                pet_info_text.set("\n连接中...请等待！")
            time.sleep(1)


def cave_mine():
    if need_stop:
        return
    try:
        挖矿(0)
        挖矿(1)
        if 剩余挖矿时间() < 48.00:
            挖矿(2)  # 自动加时
    except:
        pass
    cavemine_thread = threading.Timer(5, cave_mine)
    cavemine_thread.start()


def on_closing():
    global need_stop
    # 处理关闭窗口事件的代码
    app.destroy()  # 销毁窗口
    need_stop = 1


def init_loop():
    time.sleep(1)
    threading.Thread(target=get_login).start()


def on_room_change(event):
    num = escape_entry_manual_roomid.get()
    room_name = get_real_room(num)
    if room_name:
        escape_label_room_name_text.config(text=room_name)
    else:
        escape_label_room_name_text.config(text="")


def get_rocks_logs():
    test = ""
    logs_list = get_gift_logs()["list"][:3]
    for i in logs_list:
        rocks = float(i["rocks"])
        test += f"{i['datetime']} {i['rocks']} \n{'收到' if rocks > 0 else '赠送'} ID:{i['userId']} 昵称:{i['nickname']} \n\n"
    get_rocks_logs_text.set(test)


if "__main__" == __name__:
    # 创建窗口
    app = tk.Tk()
    app.geometry("370x500")
    app.title("登录中 - 方块兽")
    app.resizable(False, False)

    # 创建变量
    pet_info_text = tk.StringVar()
    escape_wacth_textarea_text = tk.StringVar()
    get_rocks_logs_text = tk.StringVar()

    # 修改图标
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(favicon.img))
    tmp.close()
    app.iconbitmap("tmp.ico")
    os.remove("tmp.ico")

    # 创建Tabs
    ui_tab = ttk.Notebook(app)

    # guaji页面
    frame_guaji = tk.Frame(width=500, height=500)
    pet_info_textarea = tk.Label(
        frame_guaji,
        textvariable=pet_info_text,
        anchor="w",
        justify="left",
        font=("黑体", 12),
    )
    pet_info_textarea.place(x=0, y=0)
    ui_tab.add(frame_guaji, text="乌龟-挂机")

    # 逃杀监控页面
    frame_escape_wacth = tk.Frame()
    escape_wacth_textarea = tk.Label(
        frame_escape_wacth,
        textvariable=escape_wacth_textarea_text,
        anchor="w",
        justify="left",
        font=("黑体", 12),
    )
    escape_wacth_textarea_text.set("")
    escape_wacth_textarea.place(x=0, y=0)
    escape_button_start = tk.Button(
        frame_escape_wacth, text="开始监控", command=start_escape_wacth
    )
    escape_button_start.place(x=10, y=20)
    escape_label_manual = tk.Label(frame_escape_wacth, text="手动模式:")
    escape_label_manual.place(x=10, y=290)
    escape_label_manual_roomid_text = tk.Label(frame_escape_wacth, text="房间号:")
    escape_label_manual_roomid_text.place(x=10, y=320)
    escape_entry_manual_roomid = tk.Entry(frame_escape_wacth)
    escape_entry_manual_roomid.bind("<KeyRelease>", on_room_change)
    escape_entry_manual_roomid.place(x=100, y=320)
    escape_label_room_name_text = tk.Label(frame_escape_wacth, text="")
    escape_label_room_name_text.place(x=280, y=320)
    escape_label_manual_num_text = tk.Label(frame_escape_wacth, text="投入宝石:")
    escape_label_manual_num_text.place(x=10, y=350)
    escape_entry_manual_num = tk.Entry(frame_escape_wacth)
    escape_entry_manual_num.place(x=100, y=350)
    escape_button_manual_start = tk.Button(frame_escape_wacth, text="投入")
    escape_button_manual_start.place(x=10, y=390)
    ui_tab.add(frame_escape_wacth, text="逃杀-监控")

    # 宝石
    frame_rocks = tk.Frame()
    login_label_phone = tk.Label(frame_rocks, text="用户 ID:")
    login_label_phone.place(x=10, y=10)
    login_entry_phone = tk.Entry(frame_rocks)
    login_entry_phone.place(x=90, y=10)
    login_label_user_name = tk.Label(frame_rocks, text="未查询")
    login_label_user_name.place(x=260, y=10)
    login_label_code = tk.Label(frame_rocks, text="赠送数量:")
    login_label_code.place(x=10, y=40)
    login_entry_code = tk.Entry(frame_rocks)
    login_entry_code.place(x=90, y=40)
    login_button_get_code = tk.Button(frame_rocks, text="查询用户名")
    login_button_get_code.place(x=10, y=80)
    login_button_login = tk.Button(frame_rocks, text="赠送")
    login_button_login.place(x=110, y=80)
    login_label_log = tk.Label(frame_rocks, text="宝石记录")
    login_label_log.place(x=10, y=130)
    login_button_get_log = tk.Button(
        frame_rocks, text="查询最近3条", command=get_rocks_logs
    )
    login_button_get_log.place(x=100, y=125)
    login_text_logs = tk.Label(
        frame_rocks,
        textvariable=get_rocks_logs_text,
        anchor="w",
        justify="left",
        font=("黑体", 12),
    )
    login_text_logs.place(x=0, y=170)
    ui_tab.add(frame_rocks, text="宝石")

    # 登录页面
    frame_login = tk.Frame()
    login_label_phone = tk.Label(frame_login, text="手机号:")
    login_label_phone.place(x=10, y=10)
    login_entry_phone = tk.Entry(frame_login)
    login_entry_phone.place(x=80, y=10)
    login_label_code = tk.Label(frame_login, text="验证码:")
    login_label_code.place(x=10, y=40)
    login_entry_code = tk.Entry(frame_login)
    login_entry_code.place(x=80, y=40)
    login_button_get_code = tk.Button(frame_login, text="获取验证码", command=send_code)
    login_button_get_code.place(x=10, y=80)
    login_button_login = tk.Button(frame_login, text="登录", command=login)
    login_button_login.place(x=100, y=80)
    login_text_token = tk.Text(
        frame_login, height=10, width=50, font=("黑体", 12), bg="#F0F0F0", bd=0
    )
    login_text_token.place(x=0, y=130)
    ui_tab.add(frame_login, text="登录")

    # 放置Tabs
    ui_tab.place(x=0, y=0)

    app.protocol("WM_DELETE_WINDOW", on_closing)

    threading.Thread(target=init_loop).start()

    app.mainloop()
