#coding:utf-8
'''
ping demo
计算ping的延时
'''
import multiprocessing
import re
import subprocess
import datetime
import sys,os

def pinger(ip):
    cmd = 'ping -n 2 %s' % (ip.strip())
    ret = subprocess.getoutput(cmd)
    loss_re = re.compile(r"\((.*) 丢失\)，")
    packet_loss = loss_re.findall(ret)[0]
    rtt_re = re.compile(r"最短 = (.*)，最长 = (.*)，平均 = (.*)")
    rtts = rtt_re.findall(ret)
    all = rtts[0]
    rtt_min=all[0]
    rtt_avg=all[0]
    rtt_max=all[0]
    print("%s\t\t%s\t\t%s\t\t%s\t\t%s"%(ip,packet_loss,rtt_min,rtt_max,rtt_avg))

if __name__ == '__main__':
    if not os.path.exists("hosts.txt"):
        print("\033[31mhosts.txt文件不存在，请重试\033[0m")
        sys.exit(1)
    now = datetime.datetime.now()
    file=open('hosts.txt','r')
    pool=multiprocessing.Pool(processes=4)
    result=[]
    print("########%s###########" % now)
    print("IPADDRSS\t\t\tLOSS\t\tMIN\t\tMAX\t\tAVG")
    for i in file.readlines():
        if len(i) == 1 or i.startswith("#"):
            continue
        result.append(pool.apply_async(pinger,(i.strip(),)))
    pool.close()
    pool.join()