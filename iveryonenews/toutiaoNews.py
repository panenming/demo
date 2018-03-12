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

def get_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.execute_script("window.scrollBy(0, 5000)", "")
    time.sleep(3)
    page = driver.page_source
    driver.close()
    return page

def read_item_url(url):   
    news_list = []
    link_head = 'http://toutiao.com'
    soup = BeautifulSoup(get_page(url))
    items = soup.find_all("div", {"class", "item-inner"})

    for i in range(0, len(items)):
        if len(items[i].select('img')) == 0:
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            source = items[i].find_all('div', {"class": re.compile("lfooter$")})[0].find_all(
                '', {"class": re.compile("^((?!source).)+$")})[0].get_text().strip().encode('GBK', 'ignore')
            news = News('', '', '', title, source, link)
        if len(items[i].select('img')) == 1:
            image = items[i].select('img')[0].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            source = items[i].find_all('div', {"class": re.compile("lfooter$")})[0].find_all(
                '', {"class": re.compile("^((?!source).)+$")})[0].get_text().strip().encode('GBK', 'ignore')
            news = News(image, '', '', title, source, link)
        if len(items[i].select('img')) == 3:
            image1 = items[i].select('img')[0].get('src')
            image2 = items[i].select('img')[1].get('src')
            image3 = items[i].select('img')[2].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            source = items[i].find_all('div', {"class": re.compile("lfooter$")})[0].find_all(
                '', {"class": re.compile("^((?!source).)+$")})[0].get_text().strip().encode('GBK', 'ignore')
            news = News(image1, image2, image3, title, source, link)
        news_list.append(news)
    return news_list
        

def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")

def get_keyword_news(key,page,count):
    url = "https://www.toutiao.com/search_content/?offset=%s&format=json&keyword=%s&count=%s"%(key,page,count)
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

    read_item_url('http://toutiao.com/group/6531710434200781315/')
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