'''
Created on 2017年10月17日

@author: SunYawei
'''
#from set_util import *
from pybloom import BloomFilter
import jieba
from math import *
import jieba.analyse

def get_shingles(title):
    jieba.analyse.set_stop_words('D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt')
    seg = jieba.analyse.extract_tags(title,5)
    #seg = list(jieba.cut(title))
    fr = open('D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt',encoding='utf-8')
    stopw = [line.strip() for line in fr.readlines()]
    shingles = set(seg) - set(stopw) - set(" ")
    return shingles


def cal_similar_degree(title0, title1):
    shingles0 = get_shingles(title0)#计算doc的shingles
    shingles1 = get_shingles(title1)
    #求shingles0,shingles1的交集
    #shingles01_and = set_and(shingles0, shingles1)
    #求shingles0,shingles1的并集
    shingles01_or = set_or(shingles0, shingles1)
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
    #c01 = 1.0 * len(shingles01_and) / len(shingles0)#计算doc0对doc1的包含度
    #c10 = 1.0 * len(shingles01_and) / len(shingles1)#计算doc0对doc1的包含度
    return similar_rate

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


doc0 = '习近平出席APEC峰会并发表主旨演讲'
doc1 = '习近平主席在亚太经合组织工商领导人峰会上的主旨演讲'
cal_similar_degree(doc0, doc1)


# 默认同一个新闻源内部不会有重复或相似新闻
# source1: {newsID:[title,num],...}
def dropSimilarNews(source1,source2):
    mergedList = []
    for news1,list1 in source1.items():
        title1 = list1[0]
        num1 = list1[1]
        flag = 1
        for news2,list2 in source2.items():
            title2 = list2[0]
            num2 = list2[1]
            similar = cal_similar_degree(title1,title2)
            if similar>=0.4:
                print(similar)
                flag = 0
                if num1 >= num2:
                    mergedList.append(news1)
                    del source2[news2]
                else:
                    mergedList.append(news2)
                    del source2[news2]
                break
        if flag == 1:
            mergedList.append(news1)
            
    # 添加剩余没重复的
    for news2 in source2:
        mergedList.append(news2)       
                
    return mergedList

'''
source1 = {"1":["美国第一夫人登上长城 获赠“好汉证”",400],"2":["美俄互指对方违反《中导条约 分析：或陷入新冷战",500]}   
source2 = {"3":["美俄再次互怼 指对方违反《中导条约》",200],"4":["美第一夫人登长城顺利拿下“好汉证”",300]}
list = dropSimilarNews(source1, source2)
print(list)  
'''