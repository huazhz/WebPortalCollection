# -*- coding: utf-8 -*-
'''
Created on 2017年10月30日

@author: SunYawei
'''
import jieba.analyse
import jieba.posseg as pseg

# allnews:{newsID:title}
def mysql_newstag(allnews,path):
    newsTags = {}
    for newsID,title in allnews.items():
        tags = ''
        #设置过滤停用词
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
        newsTags[newsID] = tags
    return newsTags

if __name__ == '__main__' :
    path = 'D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt'
    allnews = {'1':'习近平APEC工商领导人峰会讲话引热烈反响'}
    print(mysql_newstag(allnews,path)['1']) 
               