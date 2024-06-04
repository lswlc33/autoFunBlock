import base64
import tkinter as tk
from tkinter import DISABLED, ttk
import threading, time
from lib.乌龟 import *
from lib.宝石矿洞 import *
from lib.登录信息 import *
from lib.贝壳 import 贝壳市场
from lib.账号 import 发送验证码, 登录, 验证token
import res.favicon as favicon
from lib.雪の函数 import is_time_to_sleep, 当前时间


def send_code():
    res = 发送验证码(login_entry_phone.get())
    if res.get("code") == 0:
        tk.messagebox.showinfo("成功", "发送成功")
    else:
        tk.messagebox.showerror("错误", f"发送失败! {res.get('message')}")


def login():
    res = 登录(login_entry_phone.get(), login_entry_code.get())
    if res.get("errorCode") == 400:
        tk.messagebox.showerror(f"登录失败! ", "{res.get('message')}")
    else:
        tk.messagebox.showinfo("登录成功!", "token 已经写入 setting.ini")
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


def cleanT():
    pet_info_textarea.delete(1.0, tk.END)


data = ""
history = ""
乌龟ID = ""
is_sleep = 0
shell_sell_rice = 0
need_stop = 0


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
        if is_sleep:
            raise Exception("is_sleep")
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

    except Exception as e:
        print("\n刷新异常!")
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
            cleanT()
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
            pet_info_text = [
                f"\n 方块兽乌龟面板    时间: {当前时间(2)}",
                f" 乌龟自动喂养: {get_value('auto_feed')}   矿洞自动加时: {get_value('auto_extend')}",
                f"\n⨀ 我的资产\n",
                f" {data['rocks']} 宝石    {data['shells']} 贝壳约 {calc_shell_to_rock()} 宝石",
                f"\n⨀ {f'我的乌龟{{}}{{}}'.format('-睡眠中' if is_sleep else '','-捡宝中' if data['desktopDisplay'] else '-已召回')}\n\n"
                f" 乌龟ID: {data['id']}\t   组件SN: {data['sn']}",
                f" 乌龟性别：{data['gender']}\t代数: {data['generation']}",
                f" 乌龟等级: {data['level']}\t进度: {data['levelProgress']}%",
                f" 乌龟战力: {data['combatPower']}",
                f" 耐力: {data['stamina']}  速度: {data['speed']}  力量: {data['strength']}  幸运: {data['luck']}",
                f" 饥饿: {data['hunger']}   干净: {data['cleanliness']}   健康: {data['healthiness']}",
                f" 探测器: {data['detector']}级",
                f"\n⨀ {f'最新报告: {{}}'.format(history['list'][0]['date'])}\n",
                f" 今日时长: {history['list'][0]['duration']}\n"
                f" 今日预计: {round(时薪*16,3)} 宝石   时薪: {round(时薪,3)} 宝石\n"
                f" 今日获取: {data['todayRocks']} 宝石   {data['todayShells']} 贝壳",
                f"\n⨀ 开源项目\n",
                f" 项目地址: github.com/lswlc33/autoFunBlock ",
            ]
            for i in pet_info_text:
                pet_info_textarea.insert(tk.END, i + "\n")
            if bool(get_value("auto_feed")) and not is_sleep:
                if int(data["hunger"]) < 78:
                    乌龟喂养(乌龟ID)
                    乌龟清理(乌龟ID)

            time.sleep(1)
        except Exception as e:
            if data != "":
                print(f"\n刷新异常!\n{e}")
            else:
                pet_info_textarea.insert(tk.END, "\n连接中...请等待！")
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


if "__main__" == __name__:
    # 创建窗口
    app = tk.Tk()
    app.title("登录中 - 方块兽")
    app.resizable(False, False)

    # 修改图标
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(favicon.img))
    tmp.close()
    app.iconbitmap("tmp.ico")
    os.remove("tmp.ico")

    # 创建Tabs
    ui_tab = ttk.Notebook(app)

    # guaji页面
    frame_guaji = tk.Frame(width=100, height=100)
    pet_info_textarea = tk.Text(
        frame_guaji, height=28, width=50, font=("黑体", 12), bg="#F0F0F0", bd=0
    )
    pet_info_textarea.pack()
    ui_tab.add(frame_guaji, text="乌龟-挂机")

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
    ui_tab.pack()

    app.protocol("WM_DELETE_WINDOW", on_closing)

    threading.Thread(target=init_loop).start()

    app.mainloop()
