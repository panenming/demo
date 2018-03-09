#coding:utf-8
import re
import os
import time
import codecs
import requests
import datetime
from bs4 import BeautifulSoup
import chardet

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
        title = soup.find('meta', property="og:title").get("content")
        
        div_lelvel_str = soup.find('div', id='article')
        p_level_list = div_lelvel_str.find_all('p')
        content = ""
        for item in p_level_list:
            content = content + item.text.strip()+'\n'
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
        for page_num in range(start_page_num, start_page_num+5):
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

if __name__ == '__main__':
    valid_timestamp_url_list = get_realtime_news()
    for url in valid_timestamp_url_list:
        title,content = read_item_url(url)
        if content:
            print(title,content)
        else:
            continue
        
    # print(valid_timestamp_url_list)