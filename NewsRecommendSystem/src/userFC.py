# -*- coding: utf-8 -*-
'''
Created on 2017年10月15日

@author: SunYawei
'''
import math
from numpy.lib.financial import rate

#   计算用户相似相关性
def calcSimlaryCosDist(user1,user2):
    sum_x=0.0
    sum_y=0.0
    sum_xy=0.0
    avg_x=0.0
    avg_y=0.0
    for key in user1:
        avg_x+=float(key[1]) 
    avg_x=avg_x/len(user1)
    
    for key in user2:
        avg_y+=float(key[1])
    avg_y=avg_y/len(user2)
    
    for key in user1:
        sum_x+=(float(key[1])-avg_x)**2
        
    for key in user2:
        sum_y+=(float(key[1])-avg_y)**2
    
    for key1 in user1:
        for key2 in user2:
            if key1[0]==key2[0] :
                sum_xy+=(float(key1[1])-avg_x)*(float(key2[1])-avg_y)
        #sum_x+=(float(key1[1])-avg_x)*(float(key1[1])-avg_x)
    
    if sum_xy == 0.0 :
        return 0
    sx_sy=math.sqrt(sum_x*sum_y) 
    return sum_xy/sx_sy

#
#   计算与指定用户最相近的邻居
#   对两个没有交集的用户不需要比较
#   输入:指定用户ID，所以用户数据，所以物品数据
#   输出:与指定用户最相邻的邻居列表
#
def calcNearestNeighbor(userid,users_dic,item_dic):
    neighbors=[]
    #neighbors.append(userid)
    #获得与其有交集的用户
    for key in users_dic[userid]:
        for neighbor in item_dic[key[0]]:
            if neighbor != userid and neighbor not in neighbors: 
                neighbors.append(neighbor)
      
    neighbors_dist={}
    for neighbor in neighbors:
        dist=calcSimlaryCosDist(users_dic[userid],users_dic[neighbor])  
        neighbors_dist[neighbor] = dist
    dict_sort = sorted(neighbors_dist.items(), key = lambda x:x[1] , reverse=True)
    #将排好序的数组转成字典
    neighbors_dic={}
    for i in dict_sort:
        neighbors_dic[i[0]] = i[1]
    #返回排好序的neighbors_dic字典
    return  neighbors_dic

#   生成用户评分的数据结构
#   输入:数据 {id1:[[key1,rate1],[key2,rate2],...],...}
#   输出:数据{key1:[id1,id2,...],...}
def createUserRankDic(rates):
    user_rate_dic={}#用户字典
    item_to_user={}#类型字典
    for i in rates:
        user_rank=(i[1],i[2])
        if i[0] in user_rate_dic.key():
            user_rate_dic[i[0]].append(user_rank)
        else:
            user_rate_dic[i[0]]=[user_rank]
            
        if i[1] in item_to_user:
            item_to_user[i[1]].append(i[0])
        else:
            item_to_user[i[1]]=[i[0]]
            
    return user_rate_dic,item_to_user

#   每次每人推荐40条，用户标签混合推荐
#   user_to_news:所有用户的一天内新闻点击数据,每个元素包含一个用户今日看过新闻的集合
#   all_news:所有最新新闻,元素格式[id,tags,scores,kind],其中tags是标签集合
#   每次产生一组新闻
def recommendByUserFC(userid,user_to_rate,key_to_user,user_to_key,user_to_news,all_news):   
    #获取neighbors字典 
    All_neighbors=calcNearestNeighbor(userid,user_to_rate,key_to_user)
    #获取前20名用户
    neighbors = {}
    k = 0
    for neighbor,rate in All_neighbors.items():
        neighbors[neighbor] = rate
        k += 1
        if k == 20:
            break
        
    #生成新闻推荐标签:
    #key:tag; value:score;     
    recommend_tag={}
    #现将用户自己现有的tag添加进去
    for list in user_to_rate[userid]:
        recommend_tag[list[0]] = int(list[1])
    for neighbor in neighbors:
        tags=user_to_rate[neighbor]
        for tag in tags:
            #print movie
            if tag[0] not in recommend_tag:
                recommend_tag[tag[0]] = 1
            else:
                recommend_tag[tag[0]] += 0.05*neighbors[neighbor]
    print(recommend_tag)
    
    #用户圈新闻推荐
    user_recommend_news={}
    #添加相似用户看过的新闻
    for neighbor in neighbors:
        #news为新闻的id
        for news in user_to_news[neighbor]:
            #将neighbor用户看过的新闻推荐给该用户
            if news not in user_recommend_news and news not in user_to_news[userid]:
                #新闻推荐指数
                score = 0
                for neighbor in neighbors.keys():
                    #搜寻看过该新闻的neighbor
                    if news in user_to_news[neighbor]:
                        score += neighbors[neighbor]    
                user_recommend_news[news] = score    
    #将user_recommend_news里的新闻按score降序排序
    user_recommend_news = sorted(user_recommend_news.items(), key = lambda x:x[1] , reverse=True)
    recommend_list_byUser = []
    for news in user_recommend_news:
        recommend_list_byUser.append(news)    
        
    #依照推荐tags生成初步新闻list
    #key:news; value:score            
    tag_recommend_news={}
    for news,tags in all_news.items():
        for tag in tags:
            if tag in recommend_tag:
                #给recommend_tag评分
                if news not in tag_recommend_news:
                    tag_recommend_news[news] = recommend_tag[tag]
                else:
                    tag_recommend_news[news] += recommend_tag[tag]
    #将tag_recommend_news里的新闻按各自score降序排序
    tag_recommend_news = sorted( tag_recommend_news.items(), key = lambda x:x[1] , reverse=True)
    recommend_list_byTag = []
    for news in tag_recommend_news:
        recommend_list_byTag.append(news)    
    
    length = len(recommend_list_byUser)
    if length>=40:
        return recommend_list_byUser
    else:
        mixedRecommend = recommend_list_byUser + recommend_list_byTag[0:40-length]
        return mixedRecommend

if __name__ == '__main__' :
    userID = "5218791"
    user_KeytoRate = {"5218791":[['马航',3],['马云',10],['彩虹六号',8]]}
    user_to_news = {"5218791":['1','2','3']}
    user_keys = {"5218791":['马航','马云','彩虹六号']}
    key_users = {'马航':"5218791"}
    news_to_tags = {"1":['iphone','手机']}
    recommendNews_byUser,recommendNews_byTag = recommendByUserFC(userID,user_KeytoRate,key_users,user_keys,user_to_news,news_to_tags)
    print(recommendNews_byUser)
    print(recommendNews_byTag)


