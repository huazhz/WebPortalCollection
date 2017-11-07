'''
Created on 2017年11月5日

@author: SunYawei
'''
import math
import Get_newsUser
import Get_newstag
import Global_param
import userFC
import Get_news_rate
import MySQLdb as mdb
from numpy.lib.financial import rate

# 相关新闻推荐
def recommendSimilarNews(newsID,news_to_tags,news_to_rates):
    tmpTags = news_to_tags[newsID]
    recommendNews = {}
    for news in news_to_tags:
        num = 0
        for tag in news_to_tags[news]:
            if tag in tmpTags:
                num += 1
        if num>0 and news!=newsID:
            score = num + 0.001*news_to_rates[news]
            recommendNews[news] = score
    recommendNews = sorted(recommendNews.items(), key = lambda x:x[1] , reverse=True)
    recommendList = []
    relatedNews = ""
    count = 0
    for news in recommendNews:
        recommendList.append(news[0]) 
        relatedNews = relatedNews + news[0] + '\t'
        count += 1
        if count>=10:
            break
    return recommendList,relatedNews

news_to_rates = Get_news_rate.get_news_rate()
news_to_tags = userFC.Get_newsTag()
newsID = "100648915"
recommendList,txt = recommendSimilarNews(newsID, news_to_tags, news_to_rates) 
value = [newsID,txt]

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
    cursor.execute('INSERT INTO relatednews values(%s,%s)',value)
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
