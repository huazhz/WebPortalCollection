'''
Created on 2017年11月7日

@author: SunYawei
'''

# 新用户冷处理推荐
# news_rate:新闻热度字典
# news_kind:新闻种类字典
# userInfo:{userID:[tag,kind]}
def recommendNews(news_rate,news_kind,userInfo):
    user_news = {}
    for userID,info in userInfo.items():
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
        else:
            continue
                    
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
            
        txt = ''
        # 将推荐新闻插入表中
        for i in range(20):
            for kind,news in sorted_recommendNews.items():
                txt = news[i] + '\t'
        user_news[userID] = txt
    