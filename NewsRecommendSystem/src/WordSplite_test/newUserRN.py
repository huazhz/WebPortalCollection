'''
Created on 2017年11月7日

@author: SunYawei
'''
import MySQLdb as mdb
import Get_news_rate

# 新用户冷处理推荐
def recommendNews():
    news_kind = {}
    
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
            kind = row[3]
            news_kind[news] = kind
        
        # 新闻热度字典
        news_rate = Get_news_rate.get_news_rate()
        
        sql = "SELECT * FROM usertags"
        cursor.execute(sql)
        results = cursor.fetchall()
        # 按用户依次生成推荐列表
        for row in results:
            userID = row[0]
            tags = row[1].split('\t')
            kinds = row[2].split('\t')
            recommend_News = {}
            for kind in kinds:
                recommend_News[kind] = []
            # 新用户关键词过少，利用种类推荐           
            if len(tags)<10:
                for news,kind in news_kind.items():
                    if kind in kinds:
                        recommend_News[kind].append[news]
            else:
                continue
                    
            # 新闻热度排序
            sorted_recommendNews = {}  
            for kind,list in recommend_News.items():
                news_sort = {}
                for news in list:
                    news_sort[news] = news_rate[news]
                news_sort = sorted(news_sort.items(), key = lambda x:x[1] , reverse=True)
                
                count = 0
                newlist = []
                for news in news_sort:
                    newlist.append(news[0])
                    count += 1
                    if count>= 20:
                        break
                sorted_recommendNews[kind] = newlist
            
            txt = ''
            # 将推荐新闻插入表中
            for i in range(20):
                for kind,news in sorted_recommendNews.items():
                    txt = news[i] + '\t'
            value = [userID,txt]
            cursor.execute('INSERT INTO userRN values(%s,%s)',value)
                                         
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