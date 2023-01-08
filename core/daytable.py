import numpy,xlwt
from tools import *

with open('../out/chattingAllDays.txt','r') as reader:
    chattingAllDays=json.load(reader)

dayIDFreqDict:dict[dict[float]]={}
dayKeyID=0
schoolID2id:dict[str,int]={}
dayKey2id:dict[str,int]={}
schoolIDid=0

for dayKey in chattingAllDays:
    dayKeyID+=1
    dayKey2id[dayKey]=dayKeyID
    schoolID2freq:dict[str,int]={}
    dayValue=chattingAllDays[dayKey]
    for schoolID in dayValue:
        if schoolID=='other': continue
        if not schoolID in schoolID2freq: schoolID2freq[schoolID]=0
        schoolID2freq[schoolID]+=1
    sortedFreq=sortByValue(schoolID2freq)
    freqsum:int=0
    for i in range(len(sortedFreq)):
        freqsum+=sortedFreq[i][1]
    for i in range(len(sortedFreq)):
        schoolID=sortedFreq[i][0]
        freq=sortedFreq[i][1]/freqsum
        if schoolID not in schoolID2id:
            schoolIDid+=1
            schoolID2id[schoolID]=schoolIDid
        if dayKey not in dayIDFreqDict:
            dayIDFreqDict[dayKey]={}
        dayIDFreqDict[dayKey][schoolID]=freq

#TODO: 存储

if __name__ == '__main__':
    pass