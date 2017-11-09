'''
Created on 2017年10月30日

@author: SunYawei
'''
import jieba.analyse

# allnews:{newsID:title}
def mysql_newstag(allnews):
    newsTags = {}
    for newsID,title in allnews.items():
        tag = ''
        #设置过滤停用词
        jieba.analyse.set_stop_words('D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt')
        t = jieba.analyse.extract_tags(title,4)   
        for key in t:
            tag = tag + key + '\t'
        newsTags[newsID] = tag
    return newsTags
            