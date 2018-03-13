#coding:utf-8
from random import random
import requests
import config
import time

# 刷新广告，赚取积分
def freshAd(lastid,page):
    url = "https://api.iveryone.wuyan.cn/Api/Feed/GetFeed"
    num = 0
    while True:  
        params = fixParam(lastid)
        try:
            res = requests.post(url,headers=config.HEADERS,files=params)
            if res.ok:
                if res.json().get(u"errno") == 0:
                    data = res.json().get(u"data")
                    feeds = data['feeds']
                    feedsCount = len(feeds)
                    if feedsCount > 0:
                        lastid = feeds[feedsCount-1]["feedid"]
                        print("刷新文章成功！")
                    else:
                        print("没有更多广告！")
                else:
                    print(res.text)
        except Exception:
            print("刷新失败！")
        time.sleep(3 * (random() + 1))
        num += 1
        if num == page:
            lastid = None

def fixParam(lastid):
    if lastid == None:
        params = {
            "token":(None,config.TOKEN),
            "uid":(None,config.UID),
            "lang":(None,"zh-CN")
        }
    else:
        params = {
            "token":(None,config.TOKEN),
            "uid":(None,config.UID),
            "lang":(None,"zh-CN"),
            "lastid":(None,lastid)
        }
    return params

if __name__ == '__main__':
    freshAd(None,2)
        