import numpy
from tools import *
from matplotlib import pyplot
from datetime import *

with open('../out/chattingAllDays.txt','r') as reader:
    chattingAllDays=json.load(reader)
schoolID2days={}
schoolIDs=set()

for dayKey in chattingAllDays:
    dayValue=chattingAllDays[dayKey]
    for schoolID in dayValue:
        if schoolID=='robot':continue
        schoolIDs.add(schoolID)
        if not schoolID in schoolID2days:schoolID2days[schoolID]={}

for schoolID in schoolIDs:
    for dayKey in chattingAllDays:
        if not dayKey in schoolID2days[schoolID]:
            schoolID2days[schoolID][dayKey]=0

for dayKey in chattingAllDays:
    dayValue=chattingAllDays[dayKey]
    for schoolID in dayValue:
        if schoolID=='robot':continue
        schoolID2days[schoolID][dayKey]+=1

def paint(schoolID):
    data=schoolID2days[schoolID]
    xs,ys=[],[]
    for key,value in data.items():
        xs.append(datetime.strptime(key[0:10],'%Y-%m-%d').date())
        ys.append(value)
    pyplot.figure(figsize=(10,5))
    pyplot.plot_date(xs,ys,linestyle='-',marker=',')
    pyplot.title(schoolID)
    pyplot.show()

if __name__ == '__main__':
    while True:
        try:
            schoolID=input('请输入您想了解的学号:')
            paint(schoolID)
        except KeyError:
            print('输入错误,请重新输入!')
