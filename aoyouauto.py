import win32api
import win32con
import time

def click(keys):
    for i in range(len(keys)):
        keyClick(keys[i])
    for i in range(len(keys)):
        keyUp(keys[i])

def keyClick(key):
    win32api.keybd_event(key,0,0,0)

def keyUp(key):
    win32api.keybd_event(key,0,0,0)

while True:
    # 按下 tab 切换遨游浏览器 页签
    # ctrl + tab
    keys = [17,9]
    click(keys)
    # F5 按键
    keys = [116]
    click(keys)
    time.sleep(3)