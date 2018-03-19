import config
import requests
def userinfo():
    url = "http://api.qianmishenghuo.com/user/info"
    
    try:
        res = requests.get(url,headers=config.HEADERS)
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
    userinfo()