import numpy as np
import pandas as pd
import pendulum

datafile = "jira/close.xlsx"
datareult= "jira/result.xlsx"
parties = ['id',
           'errlevel',
           'createtime']

starttime = '2018/01/01'

start_date = pendulum.create(2018,1,1)
def init(result,start_date):
    result[starttime] = 0
    for i in range(364):
        # print('1')
        time = start_date.add(days=i)
        result[time.format('%Y/%m/%d')] = 0


data = pd.read_excel(datafile,names=parties)

res = data.groupby('createtime')['createtime'].count().to_dict()
result = {}
init(result,start_date)
# print(result)
for k in res:
    time = k.split('/')
    if time[1] == '一月':
        time[1] = '01'
    elif time[1] == '二月':
        time[1] = '02'
    elif time[1] == '三月':
        time[1] = '03'  
    elif time[1] == '四月':
        time[1] = '04' 
    elif time[1] == '五月':
        time[1] = '05' 
    elif time[1] == '六月':
        time[1] = '06' 
    elif time[1] == '七月':
        time[1] = '07' 
    elif time[1] == '八月':
        time[1] = '08' 
    elif time[1] == '九月':
        time[1] = '09' 
    elif time[1] == '十月':
        time[1] = '10' 
    elif time[1] == '十一月':
        time[1] = '11' 
    elif time[1] == '十二月':
        time[1] = '12'  
    time = '20' + time[2] + '/' + time[1] + '/' + time[0]
    result[time] = res[k]

pd.DataFrame(list(result.items()), columns=['time', 'count']).to_excel(datareult)
    

#print(data.groupby('createtime').count()['id'].to_excel(datareult))