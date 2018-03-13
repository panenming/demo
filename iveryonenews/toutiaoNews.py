#coding:utf-8
import re
import os
import time
import codecs
import requests
import datetime
from bs4 import BeautifulSoup
import chardet
import config
import json
from selenium import webdriver
from bean.news import News

PATH = os.path.dirname(os.path.abspath(__file__))
TIMESTAMP = time.strftime('%Y%m%d')
# yesterday = (datetime.datetime.now().date()+datetime.timedelta(days=-1)).strftime('%Y_%m_%d')

def get_page(url,driver):
    driver.get(url)
    driver.execute_script("window.scrollBy(0, 5000)", "")
    time.sleep(3)
    page = driver.page_source
    return page

def read_item_url(url,driver):  
    try:
        soup = BeautifulSoup(get_page(url,driver))

        title = soup.find("h1",attrs={"class":"article-title"}).text
        div = soup.find("div",attrs={"class":"article-content"})
        p_level_list = div.find_all("p")
        content = ""
        for item in p_level_list:
            if item.text.strip() != '':
                content = content + '<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + item.text+'</p>'
    except Exception:
        title = None
        content = None 
    
    return title,content
        

def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")

def get_keyword_news(key,page,count):
    url = "https://www.toutiao.com/search_content/?offset=%s&format=json&keyword=%s&count=%s"%(page,key,20)
    res = requests.get(headers=config.HEADERS,url=url)
    urls = []
    try:
        if res.ok:
           if res.json().get(u'message') == 'success':
               data = res.json().get(u'data')
               for item in data:
                   try:
                        url = item['article_url']
                        if url != None:
                            urls.append(url)
                   except Exception:
                       print("")                 
    except Exception as e:
        print("解析失败:",e)
    return urls

def from_jsonp(jsonp_str):
    jsonp_str = jsonp_str.strip()
    if not jsonp_str.startswith(config.JSONP_START) or \
            not jsonp_str.endswith(config.JSONP_END):
        return None
    return json.loads(jsonp_str[len(config.JSONP_START):-len(config.JSONP_END)])

if __name__ == '__main__':
    #print(get_keyword_news(config.KEYWORD,0,20))
    driver = webdriver.Chrome()
    read_item_url('http://toutiao.com/group/6531710434200781315/',driver)
    driver.close()
    # .replace('toutiao.com/group/','www.toutiao.com/a')
    #print(read_item_url("http://city.sina.com.cn/city/t/2018-03-01/110288539.html"))
    #valid_timestamp_url_list = get_realtime_news()
    #for url in valid_timestamp_url_list:
    #    title,content = read_item_url(url)
    #    if content:
    #        print(title,content)
    #    else:
    #        continue
        
    # print(valid_timestamp_url_list)