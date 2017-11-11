'''
Created on 2017年11月7日

@author: SunYawei
'''
import userFC

# 新用户冷处理(种类)推荐+用户协同关键字混合推荐
# news_rate:新闻热度字典
# news_kind:新闻种类字典
def recommendNews(news_rate,news_kind,user_kind,user_TagtoRate,tag_user,user_tag,userRecord,news_tag):
    user_news = {}
    for userID,kinds in user_kind.items():
        tags = user_tag[userID]
        recommend_News = {}
        for kind in kinds:
            recommend_News[kind] = []
            
        # 新用户关键词过少，利用种类推荐           
        if len(tags)<20:
            for news,kind in news_kind.items():
                if kind in kinds and news not in userRecord[userID]:
                    recommend_News[kind] += news                    
            # 新闻热度排序
            sorted_recommendNews = {}  
            for kind,list in recommend_News.items():
                news_sort = {}
                for news in list:
                    news_sort[news] = news_rate[news]
                news_sort = sorted(news_sort.items(), key = lambda x:x[1] , reverse=True)
                
                count = 0
                newlist = []
                for news in news_sort:
                    newlist.append(news[0])
                    count += 1
                    if count>= 20:
                        break
                sorted_recommendNews[kind] = newlist
            
            RN = []
            # 将推荐新闻插入表中
            for i in range(20):
                for kind,news in sorted_recommendNews.items():
                    if i>=len(news):
                        continue
                    RN.append(news[i])
            user_news[userID] = RN
        else:
            user_news[userID] = userFC.recommendByUserFC(userID,user_TagtoRate,tag_user,user_tag,userRecord,news_tag)
    
    # 返回字典：userID:[newsID1,newsID2,...]        
    return user_news

'''
news_rate = {'1':13,'2':24,'3':22,'4':36}
news_kind = {'1':"政治",'2':"军事",'3':"政治",'4':"科技"}
user_kind = {'1150310718':["政治","科技"],'1150310721':["政治","军事"]}
user_TagtoRate = {'1150310718':[],'1150310721':[]}
tag_user = {}
user_tag = {'1150310718':[],'1150310721':[]}
userRecord = {'1150310718':['3'],'1150310721':[]}
news_tag = {'1':['new','egg'],'2':[],'3':[],'4':[]}

userNews = recommendNews(news_rate,news_kind,user_kind,user_TagtoRate,tag_user,user_tag,userRecord,news_tag)
print(userNews)
'''
    