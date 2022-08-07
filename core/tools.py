import json,logging

def writeInfoByJson(schoolID2qq,schoolID2freq,schoolID2days,schoolID2rate,
                    chattingAllTime,chattingAllMonths,chattingAllWeeks,chattingStartTime,chattingEndTime,
                    timeDeltas,chattingAllDeltas):
    #通过JSON向文件内写入数据
    logging.info('正在写入数据......')
    with open('../out/schoolID2qq.txt','w') as writer:
        json.dump(schoolID2qq,writer)
    with open('../out/schoolID2freq.txt','w') as writer:
        json.dump(schoolID2freq,writer)
    with open('../out/schoolID2days.txt','w') as writer:
        json.dump(schoolID2days,writer)
    with open('../out/schoolID2rate.txt','w') as writer:
        json.dump(schoolID2rate,writer)
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
    with open('../out/schoolID2qq.txt','r') as reader:
        schoolID2qq=json.load(reader)
    with open('../out/schoolID2freq.txt','r') as reader:
        schoolID2freq=json.load(reader)
    with open('../out/schoolID2days.txt','r') as reader:
        schoolID2days=json.load(reader)
    with open('../out/schoolID2rate.txt','r') as reader:
        schoolID2rate=json.load(reader)
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
    return schoolID2qq,schoolID2freq,schoolID2days,schoolID2rate,\
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