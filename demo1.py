import os

import execjs
import requests
import re
session = requests.session()

def getInfo():
    url = "https://fanyi.baidu.com/#en/zh/a"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    }
    session.get(url=url,headers=headers)
    # token为空表示第一次访问百度网站服务器端没有收到baiduid cookie，会导致翻译接口校验不通过，通过刷新解决
    # 第二次访问才有token
    res = session.get(url=url,headers=headers)
    # print(res.text)
    token = re.findall("token: '.*?'",res.text)[0].split(" ")[-1][1:-1]
    i = re.findall("gtk = '.*?'",res.text)[0].split(" ")[-1][1:-1]
    return token,i

def getSign(word,i):
    with open("demo.js","r",encoding="utf-8") as f:
        ctx = execjs.compile(f.read())
    sign = ctx.call("e",word,i)
    return sign

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def spider(word,token,i):
    sign = getSign(word,i)

    data = {
        "from": "zh",
        "to": "en",
        "query": word,
        "transtype": "realtime",
        "simple_means_flag": 3,
        "sign": sign,
        "token": token,
        "domain": "common"
    }

    if is_Chinese(word) or word.isdigit():
        data['from'] = 'zh'
        data['to'] = 'en'
    else:
        data['from'] = 'en'
        data['to'] = 'en'

    url = "https://fanyi.baidu.com/v2transapi"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    }
    resp = session.post(url=url,headers=headers,data=data)
    # print(resp.json()['trans_result']['data'])
    print(resp.json()['trans_result']['data'][0]['dst'])

if __name__ == '__main__':
    os.environ['NODE_PATH'] = r"D:\nodejs\node_modules\npm\node_modules"
    token,i = getInfo()

    while True:
        word = input("请输入查询的内容: ")
        try:
            spider(word,token,i)
        except:
            print("非法内容")