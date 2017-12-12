# -*- coding: utf-8 -*-
'''
Created on 2017年11月8日

@author: SunYawei
'''
import jieba.analyse
import jieba.posseg as psg

# userTags:{userID:[[tag1,rate1],[tag2,rate2],...]}
# dayRecords:[day1,day2,..,day5]
# day1:{userID:[title1,title2,...]} 
def addUserTags(userTags,dayRecords,path):
        
    # 生成用户5天历史字典       
    userRecords = {}
    for i in range(0,5,1):
        record = dayRecords[i]
        for userID,newslist in record.items():
            if i == 0:
                userRecords[userID] = newslist
            else:
                userRecords[userID] += newslist   
                    
    # 保留用户5天内浏览过的关键词
    for userID,tags in userTags.items():
        record = userRecords[userID]
        words = ""
        for title in record:
            words += title + ','
        newTags = []
        for tag in tags:
            if tag[0] in words:
                newTags.append(tag)
        userTags[userID] = newTags     
        
    # 根据用户最新一天浏览记录更新关键词表
    records = dayRecords[4]
    # 按用户依次更新
    for userID,record in records.items():
        newslist = ""
        for title in record:
            newslist += title + ','
        jieba.analyse.set_stop_words(path)
        dayTags = jieba.analyse.extract_tags(newslist,5)
        print(dayTags)
        words = list(jieba.cut(newslist))
        oldTags_rate = userTags[userID]
        oldTags = []
        newTags = []
            
        # 更新旧key的rate
        for List in oldTags_rate:
            tag = List[0]
            rate = List[1]
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
    
    return userTags
    
if __name__ == '__main__' :
    path = 'D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt'
    userTags = {'1150310718':[['彩虹六号',3],['马云',10],['淘宝',17],['手机',20]]}  
    dayRecords = [{'1150310718':['马云在双11赚了中国人很多钱','淘宝或将取代京东成为唯一电商']},{'1150310718':['马云在双11过后成为中国首富']},{'1150310718':['iphoneX成为淘宝最热门手机']},{'1150310718':[]},{'1150310718':['马云在双11赚了中国人很多钱','淘宝或将取代京东成为唯一电商','iphoneX成为淘宝最热门手机']}]
    print(addUserTags(userTags,dayRecords,path))