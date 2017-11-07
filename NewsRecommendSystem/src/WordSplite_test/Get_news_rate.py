import Global_param
import MySQLdb as mdb

# 向mysql的allnews插入信息
def mysql_news_rate():
    fr = open(Global_param.train_set,encoding='utf-8')
    fr1 = open(Global_param.train_set,encoding='utf-8')
    news_list=[]
    news_dic={}  #字典value对应该新闻的阅读人数
    for line in fr.readlines():
        news_list.append(line.strip().split('\t')[1])
    news_list = list(set(news_list))       
    for i in news_list:
        news_dic[i]=0
    for line in fr1.readlines():
        news_dic[line.strip().split('\t')[1]]+=1
    
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
        for news in news_dic:
            value = [news,news_dic[news]] 
            cursor.execute('INSERT INTO allnews values(%s,%s)',value)
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


# 从mysql的allnews提取信息生成字典
def get_news_rate():
    news_dic = {}
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
            rate = row[1]
            news_dic[news] = rate     
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
    #print("Get_news_rate 计算新闻出现的热度")
    #print(news_dic)
    return news_dic

get_news_rate()