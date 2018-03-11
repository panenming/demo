#coding:utf-8
import sinaNews
import requests
import os
import sqlite3
import time
from random import random
import config

db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')
def uploadArticle(title,content):
    params = {
        "token":(None,config.TOKEN),
        "uid":(None,config.UID),
        "locale":(None,"undefined"),
        "title":(None,title),
        "content":(None,content),
        "author":(None,"wo"),
        "summary":(None,"我"),
        "cover":(None,"http://iveryone.wuyan.cn/cc3c717db71cebcd4ab8ea87a0154a9e.jpeg"),#写死的封面图片
        "price":(None,"1"),
        "shareAble":(None,"0"),
        "status":(None,"2")
    }
    
    res = requests.post("https://api.iveryone.wuyan.cn/Draft/Thread/Modify",headers=config.HEADERS,files=params)
    #print(res.request.body)
    #print(res.request.headers)
    if res.ok:
        if res.json().get(u"errno") == 0:
            print('上传文章成功！')
            return True
        else:
            print(res)
            return False 
    else:
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

def upload_real_time_news():
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

def upload_keyword_news():
    # 初始化db
    con = init_sqlite_db()
    # 开始分页加载新浪搜索到的新闻
    start = 1
    valid_timestamp_url_list = []
    for page in range(start,start + config.PAGECOUNT):
        for url in sinaNews.get_keyword_news(config.KEYWORD,page):
            valid_timestamp_url_list.append(url)
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
if __name__ == '__main__':
    instr = input("输入你要执行的模式（1：上传新浪的实时新闻;2：上传按关键字搜索到的新浪新闻）")
    if instr == '1':
        # 上传新浪的实时新闻
        upload_real_time_news()
    elif instr == '2':
        keyword = input("输入你要查询的关键字：")
        config.KEYWORD = keyword
        # 上传新浪的关键字新闻
        upload_keyword_news()
        ###uploadArticle(1,2)
    else:
        print("不支持该种类型！")