import re,logging
from datetime import *
logging.basicConfig(level=logging.INFO)
from tools import *

inputFilename='../in/华育校友营_3.txt'
schoolID2qq:dict[str,str]={}
qq2schoolID:dict[str,str]={}
schoolID2freq:dict[str,int]={}
schoolID2days:dict[str,list[str]]={}
schoolID2rate:dict[str,float]={}

unknown:int=0
unknownqqs:list[str]=[]

timeDelta=120
#默认如果两条消息相隔大于等于2分钟，则分属两个不同的对话part
errorDelta=1e7
#去除过于离谱的情况
maxDelta=100


weekDelta=604800#一周的秒数
weekStartTimestamp=1581782400#2020-02-16 00:00:00时的timestamp
chattingStartTimeStamp=1581859176#2020-02-16 21:19:36时的timestamp

timeDeltas:list[int]=[]

chattingEachPart:list[str]=[]
chattingStartTime:list[str]=[]
chattingEndTime:list[str]=[]
chattingAllTime:list[list[str]]=[]

chattingEachMonth:list[str]=[]
chattingAllMonths:dict[str,list[str]]={}

chattingEachWeek:list[str]=[]
chattingAllWeeks:dict[str,list[str]]={}

chattingAllDeltas:dict[int,int]={}

def generateUnknown(unknownqq):
    global unknown
    if unknownqq in qq2schoolID:
        return qq2schoolID[unknownqq]
    else:
        unknown+=1
        unknownqqs.append(unknownqq)
        return 'unknown'+str(unknown)

def searchQQ(line:str)->str:
    rline=line[::-1]
    rqq=re.search(r'(?<=[)>])[^(<]+',rline).group()
    return rqq[::-1]

def extractHead(filepath:str)->list[str]:
    with open(filepath,'r',encoding='utf-8',errors='ignore') as reader:
        txt:str=reader.read()
    return re.findall(r'20[\d-]{8}\s+[\d:]{7,8}\s+[^\n]+(?:\d{5,11}|@\w+\.[comnet]{2,3})[)>]',txt)

def extract(filepath:str):
    logging.info('正在提取数据......')
    global chattingEachPart,chattingAllTime,chattingStartTime,chattingEndTime
    global chattingEachMonth,chattingAllMonths
    global chattingEachWeek,chattingAllWeeks
    global chattingAllDeltas

    tempTime=None#上一次的发言时间
    tempMonth=None
    tempWeek=None
    _tempTime=None
    length=0
    for line in extractHead(filepath=filepath):
        time=re.search(r'20[\d-]{8}\s[\d:]{7,8}',line).group()#发言时间,YYYY-mm-dd (H)H:MM:SS
        datetimeTime=datetime.strptime(time,'%Y-%m-%d %H:%M:%S')#发言时间转化为datetime格式
        month=re.search(r'20[\d-]{5}',time).group()
        date=re.search(r'20[\d-]{8}',time).group()#发言日期,YYYY-mm-dd

        qq=searchQQ(line)#发言者的qq号
        schoolID_raw=re.search(r'(?<=[\s】])(?:1[0-9]|2[0-5]|0[89])[1-8]\d\d',line)#发言者的学号
        #计算学号时要考虑:五位学号前两位应为08<=xx<=25,第三位由于班级个数取1-8,后两位理论上来说从01-99均有可能
        if schoolID_raw is not None:schoolID:str=schoolID_raw.group()#先确定发言者是否有学号(考虑到有机器人参与)
        elif qq=='10000':schoolID="robot"#判断为机器人
        else:schoolID=generateUnknown(qq)

        if not(schoolID in schoolID2qq):schoolID2qq[schoolID]=qq#如果发言者之前没有在字典中对应qq号则进行设置
        if not(qq in qq2schoolID):qq2schoolID[qq]=schoolID
        if not(schoolID in schoolID2freq):schoolID2freq[schoolID]=0
        if not(schoolID in schoolID2days):schoolID2days[schoolID]=[]
        if not(date in schoolID2days[schoolID]):schoolID2days[schoolID].append(date)
        schoolID2freq[schoolID]+=1#发言者的发言总量+1
        schoolID2rate[schoolID]=schoolID2freq[schoolID]/len(schoolID2days[schoolID])

        if tempTime is None:
            tempTime=datetimeTime
            chattingStartTime.append(str(datetimeTime))
        delta=int(datetimeTime.timestamp()-tempTime.timestamp())
        if 0<delta<errorDelta:
            timeDeltas.append(datetimeTime.timestamp()-tempTime.timestamp())
        if 0<delta<maxDelta:
            if not delta in chattingAllDeltas:
                chattingAllDeltas[delta]=0
            chattingAllDeltas[delta]+=1
        if delta<timeDelta:#一个对话part还未结束
            chattingEachPart.append(schoolID)
        else:#一个对话part已结束,开启一个新的对话part
            chattingEndTime.append(str(tempTime))
            chattingStartTime.append(str(datetimeTime))
            chattingAllTime.append(chattingEachPart)
            chattingEachPart=[]
            chattingEachPart.append(schoolID)
        tempTime=datetimeTime#更新发言时间

        if tempMonth is None:tempMonth=month
        if tempMonth>=month:
            #这里是真的懵,有几条记录似乎没有出现在应该出现的位置,例如2020-4跑到2022-4后面了
            chattingEachMonth.append(schoolID)
        else:
            chattingAllMonths[tempMonth]=chattingEachMonth
            chattingEachMonth=[]
            chattingEachMonth.append(schoolID)
            tempMonth=month

        if tempWeek is None:tempWeek=weekStartTimestamp
        if datetimeTime.timestamp()<tempWeek+weekDelta:
            chattingEachWeek.append(schoolID)
        else:
            chattingAllWeeks[str(datetime.fromtimestamp(tempWeek))]=chattingEachWeek
            chattingEachWeek=[]
            chattingEachWeek.append(schoolID)
            tempWeek+=weekDelta

        length+=1

    chattingEndTime.append(str(tempTime))
    chattingAllTime.append(chattingEachPart)
    chattingAllMonths[tempMonth]=chattingEachMonth
    chattingAllWeeks[str(datetime.fromtimestamp(tempWeek))]=chattingEachWeek
    logging.info('提取完毕,共%d条数据'%length)

extract(filepath=inputFilename)

writeInfoByJson(schoolID2qq,schoolID2freq,schoolID2days,schoolID2rate,
                chattingAllTime,chattingAllMonths,chattingAllWeeks,chattingStartTime,chattingEndTime,
                timeDeltas,chattingAllDeltas)

if __name__ == '__main__':
    pass