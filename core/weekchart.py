import numpy
from tools import *
from matplotlib import pyplot as plt
from datetime import *

with open('../out/chattingAllWeeks.txt','r') as reader:
    chattingAllWeeks=json.load(reader)
schoolID2weeks={}
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

def paint(schoolID):
    data=schoolID2weeks[schoolID]
    xs,ys=[],[]
    for key,value in data.items():
        xs.append(datetime.strptime(key[0:10],'%Y-%m-%d').date())
        ys.append(value)
    plt.plot_date(xs,ys,linestyle='-',marker='.')
    plt.title(schoolID)
    plt.show()

if __name__ == '__main__':
    while True:
        try:
            schoolID=input('请输入您想了解的学号:')
            paint(schoolID)
        except KeyError:
            print('输入错误,请重新输入!')
