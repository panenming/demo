#coding:utf-8
from random import random
import requests
import config
import time

# 刷新广告，赚取积分
def freshAd():
    url = "https://userapi.iveryone.wuyan.cn/Api/Shadow/Query?uid=%s&token=%s&lang=zh-CN&limit=3"%(config.UID,config.TOKEN)
    res = requests.get(headers=config.HEADERS,url=url)
    if res.json().get(u"errno") == 0:
        print("刷新成功！")
        return True
    else:
        print(res.text)
        return False

if __name__ == '__main__':
    while True:
        if freshAd():
            time.sleep(2)
        else:
            time.sleep(30 * (random() + 1))
        