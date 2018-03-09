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

PATH = os.path.dirname(os.path.abspath(__file__))
TIMESTAMP = time.strftime('%Y%m%d')
# yesterday = (datetime.datetime.now().date()+datetime.timedelta(days=-1)).strftime('%Y_%m_%d')

def read_item_url(url):   
    try:
        html = requests.get(url).text.encode('ISO-8859-1')
    except BaseException:
        print('timed out in item_url;%s\n'%url)
    try:
        soup = BeautifulSoup(html, 'html5lib')
        title = soup.find('meta', property="og:title")
        if title:
            title = title.get("content")
        else:
            title = soup.find('h1',id="artibodyTitle").text
        
        div_lelvel_str = soup.find('div', id='article')
        if div_lelvel_str == None:
            div_lelvel_str = soup.find('div', id='artibody')
            
        p_level_list = div_lelvel_str.find_all('p')
        content = ""
        for item in p_level_list:
            if item.text.strip() != '点击进入专题':
                content = content + '<p>' + item.text+'</p>'
        return title,content
    except BaseException:
        return None,None

def get_realtime_news():
    now = datetime_toString(datetime.datetime.now())
    url_pattern = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=%s&r=0.30903104213777677'
    start_page_num = 1
    valid_timestamp_url_list = []
    failed_url_filename = os.path.join(PATH, 'sina_news_log')
    with codecs.open(failed_url_filename, mode='a', encoding='utf-8')as af:
        for page_num in range(start_page_num, start_page_num+config.PAGECOUNT):
            url = url_pattern%page_num
            try:
                res = requests.get(url)
                html = res.text.encode('ISO-8859-1')
            except BaseException:
                try:
                    res = requests.get(url)
                    html = res.text.encode('ISO-8859-1')
                except BaseException:
                    try:
                        res = requests.get(url)
                        html = res.text.encode('ISO-8859-1')
                    except BaseException:
                        af.write('timed out in page_url;%s\n'%url)
                        continue
            try:
                encode_type = chardet.detect(html)  
                html = html.decode(encode_type['encoding']) #进行相应解码，赋给原标识符（变量）
                page_url_list = re.findall(r'url : "(http://[a-z]+\.sina.com.cn/[a-z]+/'+ now +'/doc-[a-z]+[0-9]+\.shtml)"', html)
            except BaseException:
                af.write('div not pattern in page_url;%s\n'%url)
                continue
            for url in page_url_list:
                valid_timestamp_url_list.append(url)
    return valid_timestamp_url_list
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")

def get_keyword_news(key,page):
    url = "http://search.sina.com.cn/?q=%s&range=all&c=news&sort=time&page=%s"%(key,page)
    res = requests.get(headers=config.HEADERS,url=url)
    urls = []
    try:
        if res.ok:
           html = res.text.encode('utf-8')
           soup = BeautifulSoup(html, 'html5lib')
           result = soup.find('div',id='result')
           if result != None:
               h2 = result.find_all('h2')
               if h2 != None:
                   for h in h2:
                       try:
                           href = h.find('a').get('href')
                           if href != None:
                                urls.append(href)
                       except Exception:
                           print('找不到href')   
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
    start = 1
    for page in range(start,start + config.PAGECOUNT):
        print("第%s页"%(page))
        print(get_keyword_news(config.KEYWORD,page))
    #print(read_item_url("http://city.sina.com.cn/city/t/2018-03-01/110288539.html"))
    #valid_timestamp_url_list = get_realtime_news()
    #for url in valid_timestamp_url_list:
    #    title,content = read_item_url(url)
    #    if content:
    #        print(title,content)
    #    else:
    #        continue
        
    # print(valid_timestamp_url_list)