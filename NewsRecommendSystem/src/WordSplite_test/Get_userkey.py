'''
Created on 2017年10月28日

@author: SunYawei
'''
import jieba.analyse
import jieba.posseg as psg
import Global_param

#获取用户最近感兴趣的关键词
def Get_userkey():
    fr = open(Global_param.test_root+'test/train_date_set1.txt',encoding='utf-8')
    fr1 = open(Global_param.test_root+'test/train_date_set1.txt',encoding='utf-8')
    fw = open(Global_param.test_root+'test/user_keys.txt','w')
    users_news = {}
    
    for line in fr.readlines():
        user = line.strip().split('\t')[0]
        if user not in users_news:
            users_news[user] = []
    
    for line in fr1.readlines():
        news = line.strip().split('\t')[3]
        user = line.strip().split('\t')[0]
        users_news[user].append(news)
        
    for user,news in users_news.items():
        txt = ''
        for i in news:
            txt = txt + i + ','
        t = jieba.analyse.extract_tags(txt,Global_param.number_jieba)
        new_t = []
        
        #去除关键词中的纯数据类型
        for key in t:
            seg = list(psg.cut(key))
            if len(seg)==1:
                ele = list(seg[0])
                if ele[1] != 'm':
                    new_t.append(key)
            else:
                #排除例如"25%"这种百分数
                flag = 0
                for w in key:
                    if w == '%':
                        flag = 1
                        break
                if flag == 1:
                    continue
                new_t.append(key)
                            
        print(user,":",new_t)
        fw.write(user+'\t')
        for key in new_t:
            #添加关键词在该用户阅读新闻出现次数
            num = 0
            seg = list(psg.cut(txt))
            for ele in seg:
                w = list(ele)[0]
                if w == key:
                    num = num + 1
            if num == 0:
                num = 1
            fw.write(key+'\t'+str(num)+'\t')
        fw.write('\n')

Get_userkey()
    
    
