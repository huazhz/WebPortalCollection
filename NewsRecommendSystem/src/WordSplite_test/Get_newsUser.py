'''
Created on 2017年10月30日

@author: SunYawei
'''
import jieba.analyse
import Global_param

def Get_newsUser():
    fr = open(Global_param.test_root+'test/train_date_set1.txt',encoding='utf-8')
    fw = open(Global_param.test_root+'test/newsUsers.txt','w')
    #key:新闻id；value:所有读过新闻的用户id
    news = {}
    for line in fr.readlines():
        tag = ''
        id = line.strip().split('\t')[1]
        user = line.strip().split('\t')[0]
        if id in news.keys():
            if user not in news[id]:
                news[id].append(user)
        else:
            news[id] = []
            news[id].append(user)
    
    num = 0
    for id,users in news.items():
        txt = ''
        txt = txt + id + '\t'
        for user in users:
            txt = txt + user + '\t'
        txt = txt + '\n'
        fw.write(txt)
        num = num + 1
    return news

Get_newsUser()