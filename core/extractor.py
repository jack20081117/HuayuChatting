import re,logging
from datetime import *
logging.basicConfig(level=logging.INFO)
from tools import *

inputFilename=['../in/华育校友营_3.txt','../in/华育校友营_4.txt']
#下面几个dict存储qq和schoolID,freq,days,rate等数据的映射关系
qq2schoolID:dict[str,str]={}
qq2freq:dict[str,int]={}
qq2days:dict[str,list[str]]={}
qq2rate:dict[str,float]={}

unknown:int=0#未知学号的qq号个数
unknownqqs:list[str]=[]#未知学号的qq号

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

def generateUnknown(unknownqq):#生成未知学号的schoolID
    #原则上使用unknown1,unknown2等等
    #本来想使用字母,但后来发现unknown太多了,甚至出现了希腊字母
    global unknown
    if unknownqq in qq2schoolID:
        return qq2schoolID[unknownqq]
    else:
        unknown+=1
        unknownqqs.append(unknownqq)
        return 'unknown'+str(unknown)

def searchQQ(line:str)->str:
    #寻找消息头中蕴含的qq号信息
    #由于可能有部分人在昵称中加入半角括号,所以从消息头末尾开始匹配
    #注意这里相反,是要先找下括号")"再找上括号"("
    #结尾别忘了把找到的qq号重新倒过来
    rline=line[::-1]
    rqq=re.search(r'(?<=[)>])[^(<]+',rline).group()
    return rqq[::-1]

def extractHead(filepaths:list[str])->list[str]:
    res=[]
    for filepath in filepaths:
        with open(filepath,'r',encoding='utf-8',errors='ignore') as reader:
            txt:str=reader.read()
        res.extend(re.findall(r'20[\d-]{8}\s+[\d:]{7,8}\s+[^\n]+(?:\d{5,11}|@\w+\.[comnet]{2,3})[)>]',txt))
    return res

def extract(filepaths:list):
    #提取数据核心模块
    logging.info('正在提取数据......')
    global chattingEachPart,chattingAllTime,chattingStartTime,chattingEndTime
    global chattingEachMonth,chattingAllMonths
    global chattingEachWeek,chattingAllWeeks
    global chattingAllDeltas

    tempTime=None#上一次的发言时间
    tempMonth=None#上一次发言所在月份
    tempWeek=None#上一次发言所在周(或者说是7x86400秒)

    length=0

    for line in extractHead(filepaths=filepaths):
        time=re.search(r'20[\d-]{8}\s[\d:]{7,8}',line).group()#发言时间,YYYY-mm-dd (H)H:MM:SS
        datetimeTime=datetime.strptime(time,'%Y-%m-%d %H:%M:%S')#发言时间转化为datetime格式
        month=re.search(r'20[\d-]{5}',time).group()#发言月份,YYYY-mm
        date=re.search(r'20[\d-]{8}',time).group()#发言日期,YYYY-mm-dd

        qq=searchQQ(line)#发言者的qq号
        schoolID_raw=re.search(r'(?<=[\s】])(?:1[0-9]|2[0-6]|0[89])[1-8]\d\d',line)#发言者的学号
        #计算学号时要考虑:五位学号前两位应为08<=xx<=26,第三位由于班级个数取1-8,后两位理论上来说从01-99均有可能
        if schoolID_raw is not None:schoolID:str=schoolID_raw.group()#先确定发言者是否有学号(考虑到有机器人参与)
        elif qq=='10000' or qq=='1000000' or qq=='80000000':continue#判断为机器人(即自带系统消息)
        else:schoolID=generateUnknown(qq)#生成unknown学号
        #可能出现的一种情况是qq号内部包含了符合学号判定的字符,而此时又没有在前面加上学号
        #这种现象的一个例子是某个qq号为2489266006的人被识别为24892
        if schoolID in qq:schoolID=generateUnknown(qq)

        #如果发言者之前没有在字典中对应schoolID,qq,freq,day,rate等信息则进行设置
        if qq not in qq2schoolID:qq2schoolID[qq]=schoolID
        #可能出现的一种情况是qq之前对应了unknown学号,但现在有新的(正确)学号需要被对应
        #这种情况下要增加一个条件判断
        if qq2schoolID[qq][0]=='u':qq2schoolID[qq]=schoolID
        if qq not in qq2freq:qq2freq[qq]=0
        if qq not in qq2days:qq2days[qq]=[]
        if date not in qq2days[qq]:qq2days[qq].append(date)

        qq2freq[qq]+=1#发言者的发言总量+1
        qq2rate[qq]=qq2freq[qq]/len(qq2days[qq])

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

extract(filepaths=inputFilename)

writeInfoByJson(qq2schoolID,qq2freq,qq2days,qq2rate,
                chattingAllTime,chattingAllMonths,chattingAllWeeks,chattingStartTime,chattingEndTime,
                timeDeltas,chattingAllDeltas)

if __name__ == '__main__':
    pass