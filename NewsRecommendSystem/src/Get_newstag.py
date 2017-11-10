'''
Created on 2017年10月30日

@author: SunYawei
'''
import jieba.analyse
import jieba.posseg as pseg

# allnews:{newsID:title}
def mysql_newstag(allnews):
    newsTags = {}
    for newsID,title in allnews.items():
        tag = ''
        #设置过滤停用词
        jieba.analyse.set_stop_words('D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\stopword.txt')
        t = jieba.analyse.extract_tags(title,4)
        newT = []
        # 去除数字类关键词
        for tag in t:
            seg = list(pseg.cut(tag))
            if seg[0].flag != 'm':
                newT.append(tag)
        for key in newT:
            tag = tag + key + '\t'
        newsTags[newsID] = tag
    return newsTags
            