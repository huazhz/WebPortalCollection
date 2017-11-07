import csv
import WordSplite_test.Global_param
def Achieve_csv():
    fr = open(WordSplite_test.Global_param.test_root+'test/result_no_repeat_hot.txt',encoding='utf-8')
    #python3只支持csv文本格式输入输出
    csvf=open(WordSplite_test.Global_param.test_root+'test/test.csv','w')
    writer=csv.writer(csvf)
    i=0
    writer.writerow(['userid','newsid'])
    
    for line in fr.readlines():
       
        try :
            a=int(str(line.strip().split('\t')[0]))       
            b=int(str(line.strip().split('\t')[1]))    
            writer.writerow([a,b])
            i=i+1            
        except:
            print(line)
            continue
        
Achieve_csv()        