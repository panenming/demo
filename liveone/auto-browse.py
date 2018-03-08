import webbrowser
import time
import os
from random import choice,random
import csv


if __name__  == '__main__':
    count = 1
    all = 0
    filename = 'liveone/url.csv'
    url = []
    with open(filename,"r",encoding="gbk") as file:
        rows = csv.reader(file)
        for row in rows:
            url.append(row[0])
    openNum = 20 * random()
    print("一次打开%d个网页"%(openNum))
    ## 循环执行
    while True:
        all += 1
        count += 1
        webbrowser.open(choice(url),new=0,autoraise=True)
        print("第%d次打开"%(all))
        
        if(count == openNum):
            openNum = 20 * random()
            print("一次打开%d个网页"%(openNum))
            count = 1
            os.system('taskkill /F /IM  Maxthon.exe')
        time.sleep(30 * random())