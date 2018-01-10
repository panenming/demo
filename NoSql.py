'''

    一个 Python 的 dict 作为主要的数据存储
    仅支持 string 类型作为键 (key)
    支持存储 integer, string 和 list
    一个使用 ASCLL string 的简单 TCP/IP 服务器用来传递消息
    一些像 INCREMENT, DELETE , APPEND 和 STATS 这样的高级命令 (command)

    telnet 程序即可与服务器进行交互,

'''
'''
Commands Supported

    PUT
        参数： Key, Value
        目的： 向数据库中插入一条新的条目 (entry)
    GET
        参数： Key
        目的： 从数据库中检索一个已存储的值
    PUTLIST
        参数： Key, Value
        目的： 向数据库中插入一个新的列表条目
    APPEND
        参数： Key, Value
        目的： 向数据库中一个已有的列表添加一个新的元素
    INCREMENT
        参数： key
        目的： 增长数据库的中一个整型值
    DELETE
        参数： Key
        目的： 从数据库中删除一个条目
    STATS
        参数： 无 (N/A)
        目的： 请求每个执行命令的 成功/失败 的统计信息

COMMAND; [KEY]; [VALUE]; [VALUE TYPE]

    COMMAND 是上面列表中的命令之一
    KEY 是一个可以用作数据库 key 的 string （可选）
    VALUE 是数据库中的一个 integer, list 或 string (可选)
        list 可以被表示为一个用逗号分隔的一串 string, 比如说, “red, green, blue”
    VALUE TYPE 描述了 VALUE 应该被解释为什么类型
        可能的类型值有：INT, STRING, LIST

'''

import socket
import time
HOST = 'localhost'
PORT = 9000
SOCKET = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
STATS = {
    'PUT':{'SUCCESS':0,'ERROR':0},
    'GET':{'SUCCESS':0,'ERROR':0},
    'GETLIST':{'SUCCESS':0,'ERROR':0},
    'PUTLIST':{'SUCCESS':0,'ERROR':0},
    'INCREMENT':{'SUCCESS':0,'ERROR':0},
    'APPEND':{'SUCCESS':0,'ERROR':0},
    'DELETE':{'SUCCESS':0,'ERROR':0},
    'STATS':{'SUCCESS':0,'ERROR':0},
}



DATA = {}

def parse_message(data):
    valuedata = data.strip().split(';')
    valuelen = len(valuedata)
    command, key, value, value_type = None,None,None,None
    if valuelen == 0:
        return None,None,None
    elif valuelen == 1:
        command = valuedata[0]
    elif valuelen == 2:
        command = valuedata[0]
        key = valuedata[1]
    elif valuelen == 3:
        command = valuedata[0]
        key = valuedata[1]
        value =valuedata[2]
    elif valuelen >= 4:
        command = valuedata[0]
        key = valuedata[1]
        value = valuedata[2]
        value_type = valuedata[3]

    if value_type:
        if value_type == 'LIST':
            value = value.split(',')
        elif value_type == 'INT':
            value = int(value)
        else:
            value = str(value)
    else:
        value = None
    return command,key,value

def update_stats(command,success):
    if success:
        STATS[command]['SUCCESS'] += 1
    else:
        STATS[command]['ERROR'] += 1

def handle_put(key,value):
    DATA[key] = value
    return (True,'key [{}] set to [{}]'.format(key,value))

def handle_get(key):
    if key not in DATA:
        return (False,'error: key [{}] not found'.format(key))
    else:
        return (True,DATA[key])

def handle_putlist(key,value):
    return handle_put(key,value)

def handle_getlist(key):
    return_value = exists,value = handle_get(key)
    if not exists:
        return return_value
    if not isinstance(value,list):
        return (False,'ERROR: key [{}] contains non-list value ([{}])'.format(key,value))
    else:
        return return_value

def handle_increment(key):
    return_value = exists,value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value,int):
        return (False, 'ERROR: Key [{}] contains non-list value ([{}])'.format(
            key, value))
    else:
        DATA[key] = value + 1
        return (True, 'Key [{}] incremented to [{}]'.format(key,value))

def handle_append(key):
    return_value = exists,value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value,list):
        return (False,'ERROR: Key [{}] contains non-list value ([{}])'.format(key,value))
    else:
        DATA[key].append(value)
        return (True,'Key [{}] had value [{}] append'.format(key,value))

def handle_delete(key):
    if key not in DATA:
        return (False,'ERROR:Key not found and could not be deleted'.format(key))
    else:
        del DATA[key]

def handle_stats():
    return (True,str(STATS))



COMMAND_HANDERS = {
    'PUT':handle_put,
    'GET':handle_get,
    'GETLIST':handle_getlist,
    'PUTLIST':handle_putlist,
    'INCREMENT':handle_increment,
    'APPEND':handle_append,
    'delete':handle_delete,
    'STATS':handle_stats,
}

if __name__ == '__main__':
    SOCKET.bind((HOST,PORT))
    SOCKET.listen(1)
    while 1:
        connection,address = SOCKET.accept()
        print('{} New connection from {}'.format(
            time.strftime(("%Y/%m/%d %H:%M:%S INFO"), time.localtime()),
            address))
        data = connection.recv(4096).decode()
        # 解析命令
        try:
            command,key,value = parse_message(data)
        except:
            print('recv data:[{}]'.format(data))
            continue
        #执行命令
        if command == 'STATS':
            response = handle_stats()
        elif command in ('GET','GETLIST','INCREMENT','DELETE'):
            response = COMMAND_HANDERS[command](key)
        elif command in ('PUT','PUTLIST','APPEND'):
            response = COMMAND_HANDERS[command](key,value)
        else:
            response = (False,'unknown command type {}'.format(command))
        update_stats(command, response[0])
        data = '{};\n{}\n'.format(response[0], response[1])
        connection.sendall(bytearray(data, 'utf-8'))
        connection.close()
