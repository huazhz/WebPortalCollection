'''
Created on 2017年10月17日

@author: SunYawei
'''
#from set_util import *
from pybloom import BloomFilter

def get_shingles(doc_path, shingle_width):
    doc = open(doc_path).read()
    doc = doc.replace('\r\n', '')#去掉换行
    #doc = doc.decode('gbk')#将中文jbk转成unicode
    shingles = []#开始提取shingle
    doc_len = len(doc)
    for index in range(0,doc_len,1):
        end_index = index + shingle_width
        if end_index > doc_len:
            break
        shingles.append(doc[index : end_index])
    shingles = set(shingles)#转换为set，去掉重复的shingle
    return shingles

def cal_similar_degree(doc0, doc1):
    shingle_width = 4#shingle的宽度
    shingles0 = get_shingles(doc0, shingle_width)#计算doc的shingles
    shingles1 = get_shingles(doc1, shingle_width)
    #求shingles0,shingles1的交集
    shingles01_and = set_and(shingles0, shingles1)
    #求shingles0,shingles1的并集
    shingles01_or = set_or(shingles0, shingles1)
    similar_rate = 1.0 * len(shingles01_and) / len(shingles01_or)#计算两个文档doc0,doc1的相似性
    c01 = 1.0 * len(shingles01_and) / len(shingles0)#计算doc0对doc1的包含度
    c10 = 1.0 * len(shingles01_and) / len(shingles1)#计算doc0对doc1的包含度
    print(doc0 + '对' + doc1 + '的相似度为：' + str(similar_rate))
    print(doc0 + '对' + doc1 + '的包含度为：' + str(c01))
    print(doc1 + '对' + doc0 + '的包含度为：' + str(c10))

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


shingle_width = 4#shingle的宽度
doc0 = 'text0.txt'
doc1 = 'text1.txt'
doc2 = 'text2.txt'
cal_similar_degree(doc0, doc1)
print('----------------')
cal_similar_degree(doc1, doc2)