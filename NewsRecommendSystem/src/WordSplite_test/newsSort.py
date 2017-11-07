'''
Created on 2017年11月7日

@author: SunYawei
'''
import MySQLdb as mdb
import datetime

# 计算新闻热度
def get_NewsRate():
    timeBase = [2017,11,7,21,36]
    newsRate = {}
    
    config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'syw961018',
    'db': 'newsapp',
    'charset': 'utf8'
    }
    conn = mdb.connect(**config)
    cursor = conn.cursor()
    
    try:
        sql = "SELECT * FROM allnews"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            news = row[0]
            num = row[1]
            time = row[2]
            date = time.split(' ')[0]
            date = date.split('-')
            h = time.split(' ')[1]
            h = h.split(':')
            newsTime = [int(date[0]),int(date[1]),int(date[2]),int(h[0]),int(h[1])]   
            # 获取时间差         
            timediff = get_Timediff(newsTime, timeBase)
            score = num/100 + timediff/45000
            newsRate[news] = score
        
        # 将生成的新闻热度插入表中   
        for news in newsRate:
            value = [news,newsRate[news]] 
            cursor.execute('INSERT INTO newsrate values(%s,%s)',value)
            conn.commit()
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()
    finally:
            # 关闭游标连接
            cursor.close()
            # 关闭数据库连接
            conn.close()    
    
    

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