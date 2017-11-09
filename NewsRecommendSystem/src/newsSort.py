'''
Created on 2017年11月7日

@author: SunYawei
'''
import datetime

# 计算新闻热度
# allnews:{newsID:[num,time]}
def get_NewsRate(allnews):
    timeBase = [2017,11,7,21,36]
    newsRate = {}

    for newsID,info in allnews.items():
        num = info[0]
        time = info[1]
        date = time.split(' ')[0]
        date = date.split('-')
        h = time.split(' ')[1]
        h = h.split(':')
        newsTime = [int(date[0]),int(date[1]),int(date[2]),int(h[0]),int(h[1])]   
        # 获取时间差         
        timediff = get_Timediff(newsTime, timeBase)
        score = num/100 + timediff/45000
        newsRate[newsID] = score
    
    return newsRate   
    

# 获得时间秒差
def get_Timediff(t1, t2):
    d1 = datetime.datetime(t1[0],t1[1],t1[2],t1[3],t1[4])
    d2 = datetime.datetime(t2[0],t2[1],t2[2],t2[3],t2[4])
    d = (d1 - d2).days
    s = (d1 - d2).seconds
    if t1[3]<t2[3]:
        diff = s + (d - 1)*3600*24
    else:
        diff = s + d*3600*24
    return diff