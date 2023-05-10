import numpy,xlwt
from tools import *
from matplotlib import pyplot
from datetime import *

with open('../out/chattingAllWeeks.txt','r') as reader:
    chattingAllWeeks=json.load(reader)

def paint(weekKey,nextKey):
    schoolID2freq={}
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
         if schoolID=='other':continue
         if not schoolID in schoolID2freq:schoolID2freq[schoolID]=0
         schoolID2freq[schoolID]+=1
    sortedFreq=sortByValue(schoolID2freq)
    freqsum=0
    for i in range(len(sortedFreq)):
        freqsum+=sortedFreq[i][1]
    schoolIDList=[]
    freqList=[]
    boy,girl=0,0
    for i in range(len(sortedFreq)):
        schoolIDList.append(sortedFreq[i][0])
        freqList.append(sortedFreq[i][1]/freqsum)
        IDend=int(sortedFreq[i][0][-2])
        if 0<=IDend<=4:
            girl+=sortedFreq[i][1]
        else:
            boy+=sortedFreq[i][1]
    genders=[boy,girl]
    genders2pie=numpy.array(genders)
    freq2pie=numpy.array(freqList)
    schoolID2label=schoolIDList
    pyplot.pie(freq2pie,labels=schoolID2label,labeldistance=0.5,radius=1.2,rotatelabels=True)
    pyplot.title('%s~%s'%(weekKey[0:10],nextKey[0:10]))
    pyplot.show()

    pyplot.pie(genders2pie,labels=['boys','girls'],labeldistance=0.5,radius=1.2,rotatelabels=False)
    pyplot.title('%s~%s'%(weekKey[0:10],nextKey[0:10]))
    pyplot.show()

def getNextWeekKey(weekKey):
    week=datetime.strptime(weekKey,'%Y-%m-%d %H:%M:%S')
    nextweek=datetime.fromtimestamp(week.timestamp()+7*86400)
    return str(nextweek)

if __name__ == '__main__':
    while True:
        try:
            dayKey=input('Choose the day you want:')
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
        except Exception as e:
            print(e)
            print('输入错误,请重新输入!')