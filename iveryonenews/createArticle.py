#coding:utf-8
import sinaNews
import requests
import os
import sqlite3
import time
from random import random

db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')
token = "T5AA11FCEC25AE"# 你的token
uid = "1714420"#你的uid
def uploadArticle(title,content):
    params = {
        "token":(None,token),
        "uid":(None,uid),
        "locale":(None,"undefined"),
        "title":(None,title),
        "content":(None,content),
        "author":(None,"wo"),
        "summary":(None,"我"),
        "cover":(None,"http://iveryone.wuyan.cn/cc3c717db71cebcd4ab8ea87a0154a9e.jpeg"),#写死的封面图片
        "price":(None,"2"),
        "shareAble":(None,"0"),
        "status":(None,"2")
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"
    }
    res = requests.post("https://api.iveryone.wuyan.cn/Draft/Thread/Modify",headers=headers,files=params)
    #print(res.request.body)
    #print(res.request.headers)
    if res.json().get(u"errno") == 0:
       print('上传文章成功！')
       return True
    else:
        print(res)
        return False 

def find_in_sqlite(con,title,url):
    cursor = con.cursor()
    count = cursor.execute('''SELECT ID FROM ariticlerecord
       WHERE title='%s' AND url='%s';'''%(title,url))
    for _ in count:
        print('title=' + title + 'url=' + url + '在数据库存在，不再上传！')
        return True
    return False   
def save_in_sqlite(con,title,url):
    cursor = con.cursor()
    cursor.execute('''INSERT INTO ariticlerecord
       (title,url) VALUES('%s','%s');'''%(title,url))
    con.commit()
def init_sqlite_db():
    con = sqlite3.connect(db_file)
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ariticlerecord
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       title           TEXT    NOT NULL,
       url            TEXT     NOT NULL);''')
    con.commit()
    return con

def close_sqlite_db(con):
    if con:
        con.close()
if __name__ == '__main__':
    # 初始化db
    con = init_sqlite_db()
    # 下载新浪的数据局
    valid_timestamp_url_list = sinaNews.get_realtime_news()
    for url in valid_timestamp_url_list:
        title,content = sinaNews.read_item_url(url)
        if content:
            # 上传文章到 iveryone
            if find_in_sqlite(con,title,url):
                continue
            else:
                if uploadArticle(title,content):
                    save_in_sqlite(con,title,url)
                    # 上传成功之后，隔一段时间再上传
                    time.sleep(40 * (random() + 1))
        else:
            continue
    close_sqlite_db(con)
    
    ###uploadArticle(1,2)