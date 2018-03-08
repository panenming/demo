import sinaNews
import requests


token = "T5AA11FCEC25AE"
uid = "1714420"
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
    print(res.content)

if __name__ == '__main__':
    # 下载新浪的数据局
    valid_timestamp_url_list = sinaNews.get_realtime_news()
    for url in valid_timestamp_url_list:
        title,content = sinaNews.read_item_url(url)
        if content:
            # 上传文章到 iveryone
            uploadArticle(title,content)
        else:
            continue
    
    ###uploadArticle(1,2)