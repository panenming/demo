#coding:utf-8
TOKEN = "T5AA11FCEC25AE"#用户token
UID = "1714420"#用户uid
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"
}#请求头部信息
PAGECOUNT=1 #拉取PAGECOUNT + 1页数据
JSONP_START= r'callback('
JSONP_END = r');'
JSONP="callback"
KEYWORD="区块链"#需要在新浪新闻上搜索的词汇