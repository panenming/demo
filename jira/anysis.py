#coding:utf-8
import pandas as pd
import numpy as np
from dateutil.parser import parse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
FILEPATH = 'jira/data.csv'

def csvRead():
    parties = ['id', 'errtype',
           'errlevel', 'errname',
           'progress', 'status',
           'errlast', 'creator',
           'lasttime', 'lasttimeall',
           'costtime', 'costtimeall',
           'createtime']
    df = pd.read_csv(FILEPATH,encoding='gbk',names=parties)
    # print(df['id'][0:2])
    data = df.groupby(['status','createtime'])['id'].count()
    # print(data.query('status = \'完成\''))
    # print(df.groupby('createtime').count()['id'])
    # print(data[(data['status'] == '完成') | (data['status'] == '关闭')])
    df1 = data['关闭']
    df2 = data['完成']
    result = pd.concat(df1,df2)
    print(result)
    return df

csvRead()