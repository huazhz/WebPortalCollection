'''
Created on 2017年11月7日

@author: SunYawei
'''
import userFC

# 新用户冷处理(种类)推荐+用户协同关键字混合推荐
# news_rate:新闻热度字典
# news_kind:新闻种类字典
# userInfo:{userID:[tag,kind]}
def recommendNews(news_rate,news_kind,user_kind,user_tag,user_TagtoRate,tag_user,user_tag,userRecord,news_tag):
    user_news = {}
    for userID,info in user_kind.items():
        tags = info[0].split('\t')
        kinds = info[1].split('\t')
        recommend_News = {}
        for kind in kinds:
            recommend_News[kind] = []
        # 新用户关键词过少，利用种类推荐           
        if len(tags)<10:
            for news,kind in news_kind.items():
                if kind in kinds:
                    recommend_News[kind].append[news]                    
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
                    RN.append(news[i])
            user_news[userID] = RN
        else:
            user_news[userID] = userFC.recommendByUserFC(userID,user_TagtoRate,tag_user,user_tag,userRecord,news_tag)
    
    # 返回字典：userID:[newsID1,newsID2,...]        
    return user_news
    