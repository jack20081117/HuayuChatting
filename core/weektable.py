import numpy,xlwt
from tools import *

info=readInfoByJson()
chattingAllWeeks=info[6]

weekIDFreqDict:dict[dict[float]]={}

HuayuChatting=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=HuayuChatting.add_sheet('华育校友营',cell_overwrite_ok=True)
weekKeyID=0
schoolID2id:dict[str,int]={}
weekKey2id:dict[str,int]={}
schoolIDid=0

for weekKey in chattingAllWeeks:
    weekKeyID+=1
    weekKey2id[weekKey]=weekKeyID
    schoolID2freq:dict[str,int]={}
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
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
        if weekKey not in weekIDFreqDict:
            weekIDFreqDict[weekKey]={}
        weekIDFreqDict[weekKey][schoolID]=freq

for weekKey in chattingAllWeeks:
    weekKeyID=weekKey2id[weekKey]
    sheet.write(0,weekKeyID,weekKey)

for schoolID in schoolID2id:
    schoolIDid=schoolID2id[schoolID]
    sheet.write(schoolIDid,0,schoolID)


for weekKey in weekKey2id:
    weekKeyID=weekKey2id[weekKey]
    for schoolID in schoolID2id:
        schoolIDid=schoolID2id[schoolID]
        if schoolID in weekIDFreqDict[weekKey]:
            sheet.write(schoolIDid,weekKeyID,weekIDFreqDict[weekKey][schoolID])

HuayuChatting.save('../out/华育校友营周发言比率.xls')

if __name__ == '__main__':
    pass