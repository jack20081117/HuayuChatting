# HuayuChatting
对华育中学qq校友营的聊天记录进行清洗和分析的代码

## 分析流程和代码
### 数据提取|extractor.py
由于QQ聊天记录的高度格式化，可以较容易的用正则表达式对各类数据进行匹配。
```python
#extractor.py
import re

def extractHead(filepath:str)->list[str]:
    #filepath='../in/华育校友营_3.txt'
    with open(filepath,'r',encoding='utf-8',errors='ignore') as reader:
        txt:str=reader.read()
    return re.findall(r'20[\d-]{8}\s+[\d:]{7,8}\s+[^\n]+(?:\d{5,11}|@\w+\.[comnet]{2,3})[)>]',txt)
```
### 数据分析
#### weekchart.py&monthchart.py 周与月发言统计图
在extractor.py中，有对发言所在月份进行提取的功能：
```python
#extractor.py
month=re.search(r'20[\d-]{5}',time).group()#发言月份,YYYY-mm
date=re.search(r'20[\d-]{8}',time).group()#发言日期,YYYY-mm-dd
```
同时，对于当前发言所在周，即每隔7*86400秒更新一次:
```python
#extractor.py
weekDelta=604800#一周的秒数
```
最后，在extract函数中进行整理：
```python
#extractor.py
        if tempMonth is None:tempMonth=month
        if tempMonth>=month:
            chattingEachMonth.append(schoolID)
        else:
            chattingAllMonths[tempMonth]=chattingEachMonth
            chattingEachMonth=[]
            chattingEachMonth.append(schoolID)
            tempMonth=month
            #logging.info('读取数据至:%s'%month)

        if tempWeek is None:tempWeek=weekStartTimestamp
        if datetimeTime.timestamp()<tempWeek+weekDelta:
            chattingEachWeek.append(schoolID)
        else:
            chattingAllWeeks[str(datetime.fromtimestamp(tempWeek))]=chattingEachWeek
            chattingEachWeek=[]
            chattingEachWeek.append(schoolID)
            tempWeek+=weekDelta
```
并将结果通过json dump到HuayuChatting/out目录下的chattingAllMonths.txt和chattingAllWeeks.txt。
```python
#tools.py
import json
def writeInfoByJson(chattingAllMonths,chattingAllWeeks):
    with open('../out/chattingAllMonths.txt','w') as writer:
        json.dump(chattingAllMonths,writer)
    with open('../out/chattingAllWeeks.txt','w') as writer:
        json.dump(chattingAllWeeks,writer)
```
在weekchart.py中，通过json再次将数据从txt文件中提取出：
```python
#tools.py
def readInfoByJson()->tuple:
    with open('../out/chattingAllMonths.txt','r') as reader:
        chattingAllMonths=json.load(reader)
    with open('../out/chattingAllWeeks.txt','r') as reader:
        chattingAllWeeks=json.load(reader)
    return chattingAllMonths,chattingAllWeeks

#weekchart.py
info=readInfoByJson()
chattingAllWeeks=info[1]
```
接下来，对于提取出的数据做一些基本的处理，即根据每个月份统计每个学号出现的次数，也就是他的发言次数。
```python
#weekchart.py
info=readInfoByJson()
chattingAllWeeks=info[1]
schoolID2weeks:dict[str,dict[str,int]]={}
schoolIDs=set()

for weekKey in chattingAllWeeks:
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
        if schoolID=='robot':continue
        schoolIDs.add(schoolID)
        if not schoolID in schoolID2weeks:schoolID2weeks[schoolID]={}

for schoolID in schoolIDs:
    for weekKey in chattingAllWeeks:
        if not weekKey in schoolID2weeks[schoolID]:
            schoolID2weeks[schoolID][weekKey]=0

for weekKey in chattingAllWeeks:
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
        if schoolID=='robot':continue
        schoolID2weeks[schoolID][weekKey]+=1
```
最后，根据schoolID“定点”输出周发言统计表。这里，使用matplotlib。
```python
def paint(schoolID):
    data=schoolID2weeks[schoolID]
    xs,ys=[],[]
    for key,value in data.items():
        xs.append(datetime.strptime(key[0:10],'%Y-%m-%d').date())
        ys.append(value)
    pyplot.plot_date(xs,ys,linestyle='-',marker='.')
    pyplot.title(schoolID)
    pyplot.show()
```