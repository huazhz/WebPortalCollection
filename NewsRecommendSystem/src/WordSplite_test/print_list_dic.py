def print_dic(dic):
    f=open('D:\\学习资料\\软件工程\\大作业\\NewsRecommendSystem\\test\\result_no_repeat_hot.txt','w')
    
    for k,v in dic.items():
        if len(v)>=1:
            for i in v:
                f.write(k+'\t'+i+'\n')