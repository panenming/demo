import socket
import ssl
from pprint import pprint
import config

def openConnect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s)
    ssl_sock.connect(('api.qianmishenghuo.com', 443))
    pprint(ssl_sock.getpeercert())
    ssl_sock.send(data=bytes('{"X-TOKEN":' + config.TOKEN + '}',encoding='utf-8'))
    pprint(ssl_sock.read())

if __name__ == '__main__':
    openConnect()
