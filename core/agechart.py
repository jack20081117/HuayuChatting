import numpy
from datetime import datetime
from matplotlib import pyplot as plt
plt.rcParams['font.family']=['Microsoft YaHei']

from argparse import ArgumentParser
from tools import *

with open('../out/chattingAllWeeks.txt','r') as reader:
    chattingAllWeeks=json.load(reader)

weekIDFreqDict={}
weekAge={}

weekKeyID=0
schoolID2id={}
weekKey2id={}
schoolIDid=0

for weekKey in chattingAllWeeks:
    weekKeyID+=1
    weekKey2id[weekKey]=weekKeyID
    schoolID2freq={}
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

xs,raw_ys,ys=[],[],[]

for weekKey in chattingAllWeeks:
    weekValue=weekIDFreqDict[weekKey]
    ageSum=0
    decline=1
    for schoolID in weekValue:
        if schoolID[0]=='u':decline-=weekIDFreqDict[weekKey][schoolID]
        else:ageSum+=int(schoolID[:2])*weekIDFreqDict[weekKey][schoolID]
    xs.append(datetime.strptime(weekKey[0:10],'%Y-%m-%d').date())
    raw_ys.append(ageSum/decline)
    ys.append(0)
for i in range(len(raw_ys)):
    if i==0:
        ys[i]=(raw_ys[i]+raw_ys[i+1])/2
    elif i==len(raw_ys)-1:
        ys[i]=(raw_ys[i]+raw_ys[i-1])/2
    else:
        ys[i]=(raw_ys[i-1]+raw_ys[i]+raw_ys[i+1])/3

start,end=19,24

_xs=[datetime.strptime('20'+str(i)+'-09','%Y-%m').date() for i in range(start,end)]
_ys1=[i for i in range(start,end)]
_ys2=[i for i in range(start+4,end+4)]

if __name__ == '__main__':
    plt.figure(figsize=(10,5))
    plt.plot_date(xs,ys,linestyle='-',marker='.',label='average')
    plt.plot_date(xs,raw_ys,linestyle='--',marker=',',c='orange',label='raw')
    plt.plot(_xs,_ys1,linestyle='-',c='red',label='毕业线')
    plt.plot(_xs,_ys2,linestyle='-',c='green',label='入学线')
    plt.title('AgeChart')
    plt.legend()

    parser=ArgumentParser()
    parser.add_argument(
        "--save",
        help="Insert True if you want to save the figure else False",
        dest="save",default=None)
    args=parser.parse_args()
    save=args.save
    if save=='True':
        plt.savefig("./static/img/agechart.png")
    else:
        plt.show()