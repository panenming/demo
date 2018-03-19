import config
import requests
def hongbaolist():
    url = "http://api.qianmishenghuo.com/hongbao/claim"
    params = {
        "id":"8939",
        "type":3,
        "password":""
    }
    
    try:
        res = requests.post(url,headers=config.HEADERS,data=params)
        #print(res.request.body)
        #print(res.request.headers)
        if res.ok:
            if res.json().get(u"code") == 200:
                return res.json().get(u'data')
            else:
                print(res)
                return None 
        else:
            return None
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    hongbaolist()