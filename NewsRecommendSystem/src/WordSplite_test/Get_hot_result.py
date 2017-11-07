import Get_news_rate
import print_list_dic
import Global_param

#筛选热点新闻
def get_hot_result(top):
    f = open(Global_param.test_root+'test/result_no_repeat.txt')
    f1 = open(Global_param.test_root+'test/result_no_repeat.txt')
    #key：新闻id；value：新闻阅读次数
    news_dic=Get_news_rate.get_news_rate()
    print(news_dic)
    user_list=[]
    #key：用户id；value：新闻id
    dic={}
    for line in f.readlines():
        user_list.append(line.strip().split('\t')[0])
    user_list=list(set(user_list))
    #初始化字典
    for i in user_list:
        list1=[]
        dic[i]=list1
    
    for line in f1.readlines():
        dic[line.strip().split('\t')[0]].append(line.strip().split('\t')[1])
    
    #挑选出每个用户看过的热点新闻
    for k,v in dic.items():     
        if len(v)>3:           
            temp_list=[]         
            for j in v:
                #判断是否是热点新闻
                if news_dic[j]>top:
                    temp_list.append(j) 
            v= temp_list              
        dic[k]=v
                  
    print('Get_hot_result finished')
    #将字典写入result_no_repeat_hot.txt文件
    print_list_dic.print_dic(dic)
