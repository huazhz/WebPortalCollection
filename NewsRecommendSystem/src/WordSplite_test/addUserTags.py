'''
Created on 2017年11月8日

@author: SunYawei
'''
import MySQLdb as mdb
import jieba.analyse
import jieba.posseg as psg

def addUserTags():
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
        # value: [key,rate]
        userTags = {}
        sql = "SELECT * FROM usertags"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            userID = row[0]
            userTags[userID] = []
            tags_rate = row[1].split('\t')
            for i in range(len(tags_rate)):
                userTags[userID].append(tags_rate[i],int(tags_rate[i+1]))
        
        # 生成用户5天历史字典       
        userRecords = {}
        for i in range(1,6,1):
            sql = "SELECT * FROM userday%d"%i
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                userID = row[0]
                newslist = row[1]
                newslist = newslist.replace('\t',',')
                if i == 1:
                    userRecords[userID] = newslist
                else:
                    userRecords[userID] += newslist   
                    
        # 保留用户5天内浏览过的关键词
        for user,tags in userTags.items():
            record = userRecords[user]
            words = list(psg.cut(record))
            newTags = []
            for tag in tags:
                if tag[0] in words:
                    newTags.append(tag)
            userTags[user] = newTags     
        
        # 根据用户最新一天浏览记录更新关键词表
        sql = "SELECT * FROM userday5"
        cursor.execute(sql)
        results = cursor.fetchall()
        # 按用户依次更新
        for row in results:
            userID = row[0]
            newslist = row[1]
            newslist = newslist.replace('\t',',')
            jieba.analyse.set_stop_words('D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt')
            dayTags = jieba.analyse.extract_tags(newslist,10)
            words = list(psg.cut(newslist))
            oldTags_rate = userTags[userID]
            oldTags = []
            newTags = []
            
            # 更新旧key的rate
            for list in oldTags_rate:
                tag = list[0]
                rate = list[1]
                oldTags.append(tag)
                for word in words:
                    if word == tag:
                        rate += 1
                newTags.append([tag,str(rate)])
                
            # 添加新key
            for tag in dayTags:
                if tag not in oldTags:
                    rate = 0
                    for word in words:
                        if word == tag:
                            rate += 1
                    newTags.append([tag,str(rate)])
            userTags[userID] = newTags
    
        # 依据更新后字典更新数据库
        for userID,tags in userTags.items():
            txt = ''
            for tag in tags:
                txt = txt + tag[0] + '\t' + tag[1] + '\t'
            cursor.execute('UPDATE usertags SET tags = "%s" WHERE userID = %s' %(txt,userID))
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