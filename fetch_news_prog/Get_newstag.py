# -*- coding: utf-8 -*-
'''
Created on 2017年10月30日

@author: SunYawei
'''
import jieba.analyse
import jieba.posseg as pseg

# allnews:{newsID:title}
def get_newstag(allnews,path):
    newsTags = {}
    for newsID,title in allnews.items():
        tags = ''
        #设置过滤停用词
        jieba.Tokenizer()
        jieba.analyse.set_stop_words(path)
        t = jieba.analyse.extract_tags(title,4)
        newT = []
        # 去除数字类关键词
        for tag in t:
            seg = list(pseg.cut(tag))
            if seg[0].flag != 'm':
                newT.append(tag)
        for key in newT:
            tags = tags + key + '\t'
        newsTags[newsID] = newT
    return newsTags

def get_SearchTags(allnews):
    searchTags = {}
    for newsID,title in allnews.items():
        t = jieba.cut_for_search(title)
        searchTags[newsID] = []
        for tag in t:
            searchTags[newsID].append(tag)
    return searchTags
    

def getTags(title,path):
    jieba.Tokenizer()
    jieba.analyse.set_stop_words(path)
    seg = jieba.analyse.extract_tags(title,5)
    fr = open(path,encoding='utf-8')
    stopw = [line.strip() for line in fr.readlines()]
    shingles = set(seg) - set(stopw) - set(" ")
    return shingles

if __name__ == '__main__' :
    path = 'D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt'
    allnews = {'1':'习近平APEC工商领导人峰会讲话引热烈反响'}
    title = '习近平APEC工商领导人峰会讲话引热烈反响'
    print(get_newstag(allnews,path)['1']) 
    print(getTags(title,path))
    print(get_SearchTags(allnews))
               