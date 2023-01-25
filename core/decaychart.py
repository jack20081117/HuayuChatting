import numpy
from tools import *
from matplotlib import pyplot
from datetime import *

info=readInfoByJson()
chattingAllWeeks=info[6]
schoolID2weeks:dict[str,dict[str,int]]={}
schoolIDs=set()

decay=0.7
decayedSchoolID2weeks:dict[str,dict[str,float]]={}

for weekKey in chattingAllWeeks:
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
        if schoolID=='robot':continue
        schoolIDs.add(schoolID)
        if not schoolID in schoolID2weeks:schoolID2weeks[schoolID]={}
        if not schoolID in decayedSchoolID2weeks:decayedSchoolID2weeks[schoolID]={}

for schoolID in schoolIDs:
    for weekKey in chattingAllWeeks:
        if not weekKey in schoolID2weeks[schoolID]:
            schoolID2weeks[schoolID][weekKey]=0
        if not weekKey in decayedSchoolID2weeks[schoolID]:
            decayedSchoolID2weeks[schoolID][weekKey]=0

lastKey=None

for weekKey in chattingAllWeeks:
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
        if schoolID=='robot':continue
        schoolID2weeks[schoolID][weekKey]+=1
    for schoolID in schoolIDs:
        if lastKey is None:
            decayedSchoolID2weeks[schoolID][weekKey]=schoolID2weeks[schoolID][weekKey]
            continue
        decayedSchoolID2weeks[schoolID][weekKey]=decayedSchoolID2weeks[schoolID][lastKey]*decay+schoolID2weeks[schoolID][weekKey]
    lastKey=weekKey

def decayedPaint1(schoolID):
    data=schoolID2weeks[schoolID]
    decayedData=decayedSchoolID2weeks[schoolID]
    xs,ys=[],[]
    _key=None
    for key in data:
        value=decayedData[key]*0.9+data[key]*0.1
        if _key is not None:
            value-=0.0005*data[_key]
        _key=key
        xs.append(datetime.strptime(key[0:10],'%Y-%m-%d').date())
        ys.append(value)
    pyplot.plot_date(xs,ys,linestyle='-',marker='.')
    pyplot.title(schoolID)
    pyplot.show()

def decayedPaint2(weekKey,nextKey):
    decayedWeeks2schoolID:dict[str,dict[str,float]]={}
    xs,ys=[],[]
    for schoolID in schoolIDs:
        data=schoolID2weeks[schoolID]
        decayedData=decayedSchoolID2weeks[schoolID]
        _key=None
        for key in data:
            if key not in decayedWeeks2schoolID:decayedWeeks2schoolID[key]={}
            decayedWeeks2schoolID[key][schoolID]=decayedData[key]*0.9+data[key]*0.1
            if _key is not None:
                decayedWeeks2schoolID[key][schoolID]-=0.0005*data[_key]
            _key=key
    sortedValue=sortByValue(decayedWeeks2schoolID[weekKey])
    sortedValue=sortedValue[:8]
    for t in sortedValue:
        xs.append(t[0])
        ys.append(t[1])
    pyplot.bar(xs,ys)
    pyplot.title('%s~%s'%(weekKey[:10],nextKey[:10]))
    pyplot.show()

if __name__ == '__main__':
    while True:
        try:
            schoolID=input('请输入您想了解的学号:')
            decayedPaint1(schoolID)

            dayKey=input('Choose the day you want:')
            dayKey+=' 00:00:00'
            lastKey=None
            for weekKey in chattingAllWeeks:
                if lastKey is None:
                    lastKey=weekKey
                    weekKey='2020-02-23 00:00:00'
                if lastKey<=dayKey<=weekKey:
                    decayedPaint2(lastKey,weekKey)
                    break
                lastKey=weekKey
        except KeyError as e:
            print('输入错误,请重新输入!')
            print(e)