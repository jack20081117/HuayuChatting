import numpy
from tools import *
from matplotlib import pyplot
from datetime import *
from argparse import ArgumentParser

with open('../out/chattingAllWeeks.txt','r') as reader:
    chattingAllWeeks=json.load(reader)

def paint(weekKey,nextKey):
    schoolID2freq: dict[str,int]={}
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
        if schoolID=='other': continue
        if not schoolID in schoolID2freq: schoolID2freq[schoolID]=0
        schoolID2freq[schoolID]+=1
    sortedFreq=sortByValue(schoolID2freq)
    freqsum: int=0
    for i in range(len(sortedFreq)):
        freqsum+=sortedFreq[i][1]
    schoolIDList=[]
    freqList=[]
    for i in range(len(sortedFreq)):
        schoolIDList.append(sortedFreq[i][0])
        freqList.append(sortedFreq[i][1]/freqsum)
    freq2pie=numpy.array(freqList)
    schoolID2label=schoolIDList
    pyplot.pie(freq2pie,labels=schoolID2label,labeldistance=0.5,radius=1.2,rotatelabels=True)
    pyplot.title('%s~%s'%(weekKey[0:10],nextKey[0:10]))
    pyplot.savefig("./static/img/weekpie.png")

def getNextWeekKey(weekKey):
    week=datetime.strptime(weekKey,'%Y-%m-%d %H:%M:%S')
    nextweek=datetime.fromtimestamp(week.timestamp()+7*86400)
    return str(nextweek)

if __name__=='__main__':
    arg_parser=ArgumentParser()
    arg_parser.add_argument(
        "--time",
        help="Choose the day you want",
        dest="time",default="2020-02-23")
    args=arg_parser.parse_args()
    dayKey=args.time
    dayKey+=' 00:00:00'
    lastKey=None
    for weekKey in chattingAllWeeks:
        if lastKey is None or lastKey==weekKey:
            lastKey=weekKey
            weekKey=getNextWeekKey(lastKey)
        if lastKey<=dayKey<=weekKey:
            paint(lastKey,weekKey)
            break
        lastKey=weekKey
