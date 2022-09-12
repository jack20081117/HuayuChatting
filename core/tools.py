import json,logging

def writeInfoByJson(qq2schoolID,qq2freq,qq2days,qq2rate,
                    chattingAllTime,chattingAllMonths,chattingAllWeeks,chattingStartTime,chattingEndTime,
                    timeDeltas,chattingAllDeltas):
    #通过JSON向文件内写入数据
    logging.info('正在写入数据......')
    with open('../out/qq2schoolID.txt','w') as writer:
        json.dump(qq2schoolID,writer)
    with open('../out/qq2freq.txt','w') as writer:
        json.dump(qq2freq,writer)
    with open('../out/qq2days.txt','w') as writer:
        json.dump(qq2days,writer)
    with open('../out/qq2rate.txt','w') as writer:
        json.dump(qq2rate,writer)
    with open('../out/chattingAllTime.txt','w') as writer:
        json.dump(chattingAllTime,writer)
    with open('../out/chattingAllMonths.txt','w') as writer:
        json.dump(chattingAllMonths,writer)
    with open('../out/chattingAllWeeks.txt','w') as writer:
        json.dump(chattingAllWeeks,writer)
    with open('../out/chattingSTTime.txt','w') as writer:
        json.dump((chattingStartTime,chattingEndTime),writer)
    with open('../out/timeDeltas.txt','w') as writer:
        json.dump(timeDeltas,writer)
    with open('../out/chattingAllDeltas.txt','w') as writer:
        json.dump(chattingAllDeltas,writer)
    logging.info('写入数据完毕')

def readInfoByJson()->tuple:
    #通过JSON从文件内读入数据
    logging.info('正在读入数据......')
    with open('../out/qq2schoolID.txt','r') as reader:
        qq2schoolID=json.load(reader)
    with open('../out/qq2freq.txt','r') as reader:
        qq2freq=json.load(reader)
    with open('../out/qq2days.txt','r') as reader:
        qq2days=json.load(reader)
    with open('../out/qq2rate.txt','r') as reader:
        qq2rate=json.load(reader)
    with open('../out/chattingAllTime.txt','r') as reader:
        chattingAllTime=json.load(reader)
    with open('../out/chattingAllMonths.txt','r') as reader:
        chattingAllMonths=json.load(reader)
    with open('../out/chattingAllWeeks.txt','r') as reader:
        chattingAllWeeks=json.load(reader)
    with open('../out/chattingSTTime.txt','r') as reader:
        chattingSTTime=json.load(reader)
    with open('../out/timeDeltas.txt','r') as reader:
        timeDeltas=json.load(reader)
    with open('../out/chattingAllDeltas.txt','r') as reader:
        chattingAllDeltas=json.load(reader)
    logging.info('读入数据完毕')
    return qq2schoolID,qq2freq,qq2days,qq2rate,\
           chattingAllTime,chattingAllMonths,chattingAllWeeks,chattingSTTime,\
           timeDeltas,chattingAllDeltas

def dictKey2List(d:dict)->list:
    l=[]
    for key,value in d.items():
        l.append(key)
    return l

def dictValue2List(d:dict)->list:
    l=[]
    for key,value in d.items():
        l.append(value)
    return l

def sortByKey(d:dict)->list:
    #根据Key对Dict进行排序
    return sorted(d.items(),key=lambda t:t[0],reverse=True)

def sortByValue(d:dict)->list:
    #根据Value对Dict进行排序
    return sorted(d.items(),key=lambda t:t[1],reverse=True)

def sumOfValue(d:dict[str,int])->int:
    sum:int=0
    for key,value in d.items():
        sum+=value
    return sum

def transferList(l:list,src,target)->list[str]:
    for i in range(len(l)):
        item=l[i]
        if isinstance(item,list):
            l[i]=transferList(item,src,target)
        elif isinstance(item,str):
            if item==src:
                l[i]=target
    return l