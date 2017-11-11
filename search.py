# -*-coding:utf-8-*-
    
# import test1.Spider as Spider
import jieba
import pymysql

conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='lijiaming',db='NEW',charset='utf8')
stopw = [line.strip() for line in open("stop.txt", encoding = "utf-8")]
stopw = set(stopw)

#切分题目
def CutTitle():
    cursor = conn.cursor()
    sql = "select * from news"
    
    dict = {}
    dict2 = {}
    
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        
        for row in res:
            id = str(row[0])
            title = row[1]
            #seg_list为jieba分词结果
            seg_list = jieba.cut_for_search(title)
            temp = "/".join(set(seg_list) - stopw)
            title = temp.split(sep="/")
            dict2[id] = []
            for i in title:
                dict2[id].append(i)
                
                if(i in dict):
#                     print('i=',i)
                    dict[i].append(id)
                else:
#                     print(i)
                    dict[i] = []
                    dict[i].append(id)
        
        for i in list(dict.keys()):
            for j in range(len(dict[i])/100 + 1):
                sql2 = "insert into word(word, new_id) values('%s','%s')" \
                    % (i, "/".join(dict[i][j*100:min(j*100+100-1, len(dict[i])-1)]))
                try:
                    cursor.execute(sql2)
                    conn.commit()
                except Exception as e1:
                    print("Reason:", e1)
                    conn.rollback()
                    
        for i in list(dict2.keys()):
            
            sql3 = "insert into new2word(id, word) values(%d,'%s')" % (int(i), ",".join(dict2[i])) 
                
            try:
                cursor.execute(sql3)
                conn.commit()
            except Exception as e1:
                print("Reason:", e1)
                conn.rollback()
                
    except Exception as e:
        print("Reason:", e)
    conn.close()
    
def dict2list(dic:dict):
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst
    
#新闻查询
def QueryNews(q):
    cursor = conn.cursor()
    #seg_list为jieba分词结果
    seg_list = jieba.cut_for_search(q)
#     seg_list = jieba.cut(q, cut_all = True)
#q为查询语句在分词且去除停用词之后的结果
    temp = "/".join(set(seg_list) - stopw)
    q = temp.split(sep="/")
    
    print("cut ok")
    
    dict = {}
    
    for i in q:
        #依次查找q中的每一个词所出现在的新闻
        sql = "select * from word where word = '%s'" % i
        
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                id = row[1]
                id_set = id.split("/")
                for j in id_set:
                    if(j in dict):
                        #每命中依次，改新闻hit次数加一，存于dict字典中
                        dict[j] += 1
                    else:
                        dict[j] = 1
        
        except Exception as e1:
            print("Reason:", e1)
            
    #对dict按照hit次数排序
    dic = sorted(dict2list(dict), key=lambda x:x[1], reverse=True)    

    #取出查询新闻结果
    for i in dic:
#         print(i)
        sql = "select * from news where id = %d" % int(i[0])
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                title = row[1]
                url = row[2]
                print(title)
                print(url)
        
        except Exception as e1:
            print("Reason:", e1)
        
    print(q)

if __name__ == "__main__":
    # CutTitle()
    
#     q = input("搜索：")
#     QueryNews(q)

    
    
    
