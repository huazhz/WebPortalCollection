'''
Created on 2017年10月30日

@author: SunYawei
'''
import jieba.analyse
import Global_param
import MySQLdb as mdb

def mysql_newstag():
    fr = open(Global_param.test_root+'test/train_date_set1.txt',encoding='utf-8')
    
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
        news = []
        for line in fr.readlines():
            tag = ''
            id = line.strip().split('\t')[1]
            if id in news:
                continue
            else:
                news.append(id)
            txt = line.strip().split('\t')[3]
            #设置过滤停用词
            jieba.analyse.set_stop_words('D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt')
            t = jieba.analyse.extract_tags(txt,4)   
            for key in t:
                tag = tag + key + '\t'
            value = [id,tag]
            cursor.execute('INSERT INTO newstag values(%s,%s)',value)
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

def Get_newstag():
    news_tag = {}
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
        sql = "SELECT * FROM newstag"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            news = row[0]
            txt = row[1]
            tags = txt.strip().split('\t')
            news_tag[news] = tags 
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
    return news_tag

Get_newstag()