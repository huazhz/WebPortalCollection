# -*- coding: utf-8 -*-
'''
Created on 2017年10月17日

@author: SunYawei
'''
#from pybloom import BloomFilter
import jieba
from math import *
import jieba.analyse

def get_shingles(title,path):
    jieba.analyse.set_stop_words(path)
    seg = jieba.analyse.extract_tags(title,5)
    fr = open(path,encoding='utf-8')
    stopw = [line.strip() for line in fr.readlines()]
    shingles = set(seg) - set(stopw) - set(" ")
    return shingles


def cal_similar_degree(title0, title1, path):
    shingles0 = title0
    shingles1 = title1
    #求shingles0,shingles1的并集
    shingles01_or = list(shingles0 | shingles1)
    vector0 = []
    vector1 = []
    for word in shingles01_or:
        if word in shingles0:
            vector0.append(1)
        else:
            vector0.append(0)
        if word in shingles1:
            vector1.append(1)
        else:
            vector1.append(0)
    
    x_and_y = 0.0
    xSum = 0.0
    ySum = 0.0
    for i in range(len(vector0)):
        x_and_y += vector0[i]*vector1[i]
        xSum += vector0[i]
        ySum += vector1[i]
    similar_rate = x_and_y/sqrt(xSum*ySum)    
    return similar_rate

'''
#集合的与操作，求集合的交集
def set_and(set0, set1):
    result_set = []
    element_num = (len(set0) + len(set1)) * 10 #以set0为基准，构造布隆过滤器
    error_rate = 0.0001
    bloom = BloomFilter(element_num,error_rate)

    #将set0中的元素插入到bloom中
    for element in set0:
        element_str = str(element)
        bloom.add(element_str)
    
    #检查set1中的元素是否已经存在了
    for element in set1:
        element_str = str(element)
        if element_str in bloom:
            #已经存在了，则为要求的交集
            result_set.append(element)
    return result_set

#求集合的并集
def set_or(set0, set1):
    result_set = []
    element_num = len(set0) + len(set1)#以set0为基准，构造布隆过滤器
    error_rate = 0.0001
    bloom = BloomFilter(element_num,error_rate)

    #将set0中的元素插入到bloom中
    for element in set0:
        element_str = str(element)
        bloom.add(element_str)
        result_set.append(element)

    #检查set1中的元素是否已经存在了
    for element in set1:
        if element not in bloom:
            result_set.append(element)#还没有存在，则加入到尾部
    return result_set
'''


# 默认同一个新闻源内部不会有重复或相似新闻
# source1: {newsID:[title,num],...}
def dropSimilarNews(source1,source2,path):
    mergedList = {}
    for news1,list1 in source1.items():
        title1 = list1[0]
        num1 = list1[1]
        flag = 1
        for news2,list2 in source2.items():
            title2 = list2[0]
            num2 = list2[1]
            similar = cal_similar_degree(title1,title2,path)
            if similar>=0.5:
                #print(similar)
                #print(title1)
                #print(title2)
                flag = 0
                if num1 >= num2:
                    mergedList[news1] = [title1,num1]
                    del source2[news2]
                else:
                    mergedList[news2] = [title2,num2]
                    del source2[news2]
                break
        if flag == 1:
            mergedList[news1] = [title1,num1]
            
    # 添加剩余没重复的
    for news2,list2 in source2.items():
        mergedList[news2] = [title2,num2]       
                
    return mergedList


# source = [source1,source2,source3,source4]
def mergeAllSources(source,path):
    merge1 = dropSimilarNews(source[0],source[1],path)
    merge2 = dropSimilarNews(source[2],source[3],path)
    dic = dropSimilarNews(merge1,merge2,path)
    allmerged = []
    for news in dic:
        allmerged.append(news)
    # 返回新闻url数组
    return allmerged


if __name__ == '__main__' :
    source1 = {}
    source2 = {}
    fr1 = open("fenghuang.rec",encoding='utf-8')
    fr2 = open("tengxun.rec",encoding='utf-8')
    for line in fr1.readlines():
        info = line.split('<div/>')
        id = info[1]
        title = info[2]
        num = int(info[3])
        source1[id] = [title,num]
    for line in fr2.readlines():
        info = line.split('<div/>')
        id = info[1]
        title = info[2]
        num = int(info[3])
        source2[id] = [title,num]
    source = [source1,source2,source1,source2]
    path = 'D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt'
    #source1 = {"1":["美国第一夫人登上长城 获赠“好汉证”",400],"2":["美俄互指对方违反《中导条约 分析：或陷入新冷战",500]}   
    #source2 = {"3":["美俄再次互怼 指对方违反《中导条约》",200],"4":["美第一夫人登长城顺利拿下“好汉证”",300]}
    newslist = mergeAllSources(source,path)
    print(len(newslist))  