import Global_param

def Get_keynews(day):
    fr = open(Global_param.test_root+'test/key_words/keywords_%d.txt'%day)  #每天新闻的关键词汇总
    fr1 = open(Global_param.test_root+'test/train_date_set1/train_date_set1_%d.txt'%day)    #过去每天新闻的汇总集合
    fr2 = open(Global_param.test_root+'test/train_lastday_set/train_lastday_set1_%d.txt'%day) #部分新闻
    #以追加模式打开文档
    f = open(Global_param.test_root+'test/result.txt','a')
    list_key=[]
    dic={}  #字典的key是关键词，value是新闻id
    dic_no_repeat={}  #字典的key是用户id，value是新闻id  
    num=0
    for line in fr.readlines():
        print(line)
        for i in range(0,Global_param.number_jieba) :
            list_key.append(line.strip().split('\t')[i])
   
    for m in list_key:     
        dic[m]=[]
    
    for line in fr1.readlines():
        for j in list_key:
            #在标题中搜索关键词，如果包含则添加这条新闻
            if j in line.strip().split('\t')[3]:
                dic[j].append(line.strip().split('\t')[1])
                
    for k,v in dic.items():
        #将新闻编号拆分开来 ???
        dic[k]=list(set(v))
                        
    for line in fr2.readlines():
        list1=[]
        dic_no_repeat[line.strip().split('\t')[0]]=list1
        for k,v in dic.items():
            #在标题中搜索关键词
            if k in line.strip().split('\t')[3]:     
                #v为新闻id集合           
                for i in v:
                    #如果新闻未在用户已读列表中出现，则在该用户已读新闻列表中添加该新闻id
                    if int(i)!=int(line.strip().split('\t')[1]):
                        dic_no_repeat[line.strip().split('\t')[0]].append(i)
        #???
        dic_no_repeat[line.strip().split('\t')[0]] = list(set(dic_no_repeat[line.strip().split('\t')[0]]))       
    
    print("Get_keynews 获得与最后一次浏览相关的新闻")  
    
    for k1,v1 in dic_no_repeat.items():
        #确保用户新闻集合不为空
        if v1:
            for m in v1:
                #用户id+新闻id
                f.write(k1+'\t'+m+'\n')  
                num=num+1
             

# Get_keynews()