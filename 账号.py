import requests
from 登录信息 import write_value, get_value

headers = {
    "User-Agent": "com.caike.union/4.0.2-90585 Dalvik/2.1.0 (Linux; U; Android 14; 2211133C Build/UKQ1.230804.001)",
    "Content-Type": "application/x-www-form-urlencoded",
}


def 发送验证码(num):
    url = "https://block-api.lucklyworld.com/api/sms/send/login/code"

    payload = f"mobile={num}"

    response = requests.post(url, data=payload, headers=headers)

    return response.json()


def 登录(phone, code):
    url = "https://block-api.lucklyworld.com/api/auth/phone"

    payload = f"phone={phone}&code={code}"

    response = requests.post(url, data=payload, headers=headers)

    return response.json()


def 验证token():
    get_value("token")
    r = requests.post(
        url="https://block-api.lucklyworld.com/api/user/info",
        headers={
            "User-Agent": "com.caike.union/4.0.2-90585 Dalvik/2.1.0 (Linux; U; Android 14; 2211133C Build/UKQ1.230804.001)",
            "Content-Type": "application/x-www-form-urlencoded",
            "token": get_value("token"),
        },
    ).json()

    return r


if __name__ == "__main__":
    num = input("请输入手机号:")
    res = 发送验证码(num)
    if res.get("code") == 0:
        print("发送成功")
    else:
        print(f"发送失败! {res.get('message')}")
        exit()
        input()
    while True:
        code = input("请输入验证码:")
        res2 = 登录(num, code)
        print(res2.get("token"))
        if res.get("errorCode") == 400:
            print("登录成功! token 已经写入 setting.ini")
            write_value("token", res2.get("token"))
            break
        else:
            print(f"登录失败! {res.get('message')}")
