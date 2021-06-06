from datetime import datetime, timezone, timedelta
import requests
import os
import re

PUSH_KEY = os.getenv("PUSH_KEY")
KEY_WORD = '上海'
RK_URL = "https://bm.ruankao.org.cn/sign/welcome"
CJ_URL = "https://www.ruankao.org.cn/index/work"
CJ_KEY_WORD = r"2021年.*成绩"

def get_session(_url):
    _session = requests.Session()
    _session.headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001229) NetType/WIFI Language/zh_CN miniProgram"

    _response = _session.get(_url)
    _response.encoding = 'utf-8'

    return _response.text


def rk_status():
    _content = get_session(RK_URL)

    return 1 if KEY_WORD in _content else 0

def cj_status():
    _content = get_session(CJ_URL)
    p = re.compile(CJ_KEY_WORD)

    return 1 if len(p.findall(_content)) else 0

def notify(_title, _message=None):
    if not PUSH_KEY:
        print("未配置PUSH_KEY！")
        return

    if not _message:
        _message = _title

    _response = requests.post(
        f"https://sc.ftqq.com/{PUSH_KEY}.send", {"text": _title, "desp": _message})

    if _response.status_code == 200:
        print(f"发送通知状态：{_response.content.decode('utf-8')}")
    else:
        print(f"发送通知失败：{_response.status_code}")


def main():
    _tz = timezone(+timedelta(hours=8))
    today = datetime.now(_tz).strftime("%Y-%m-%d")
    print(datetime.now(_tz).strftime("%Y-%m-%d %H:%M"))

    if cj_status():
        print("上海软考成绩已出")
        notify("上海软考成绩已出", "已开启成绩查询通道")
    else:
        print("上海软考成绩未出")


if __name__ == "__main__":
    main()
