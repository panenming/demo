#coding:utf-8
from random import random
import requests
import config
import time

# 刷新广告，赚取积分
def freshAd():
    url = "https://api.iveryone.wuyan.cn/Api/Feed/GetFeed"
    params = {
        "token":(None,config.TOKEN),
        "uid":(None,config.UID),
        "lang":(None,"zh-CN")
    }
    
    try:
        res = requests.post(url,headers=config.HEADERS,files=params)
        if res.ok:
            if res.json().get(u"errno") == 0:
                if len(res.json().get(u"data")) > 0:
                    print("刷新文章成功！")
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
            time.sleep(3 * (random() + 1))
        else:
            time.sleep(5 * (random() + 1))
        