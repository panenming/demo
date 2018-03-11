#coding:utf-8
from random import random
import requests
import config
import time

# 刷新广告，赚取积分
def freshAd():
    url = "https://userapi.iveryone.wuyan.cn/Api/Shadow/Query?uid=%s&token=%s&lang=zh-CN&limit=3"%(config.UID,config.TOKEN)
    try:
        res = requests.get(headers=config.HEADERS,url=url)
        if res.ok:
            if res.json().get(u"errno") == 0:
                if len(res.json().get(u"data")) > 0:
                    print("刷新成功！")
                else:
                    print("没有更多广告！")
                return True
            else:
                print(res.text)
                return False
        else:
            return False
    except Exception:
        print("刷新失败！")
        return False
    

if __name__ == '__main__':
    while True:
        if freshAd():
            time.sleep(2 * (random() + 1))
        else:
            time.sleep(5 * (random() + 1))
        