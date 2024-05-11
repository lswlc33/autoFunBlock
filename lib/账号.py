import requests
from lib.登录信息 import get_value

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
