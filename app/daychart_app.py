import numpy
from tools import *
from matplotlib import pyplot
from datetime import *
from argparse import ArgumentParser

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
    pyplot.savefig("./static/img/daychart.png")

if __name__ == '__main__':
    parser=ArgumentParser()
    parser.add_argument(
        "--id",
        help="Insert the SchoolID you want to know",
        dest="id",default=None)
    args=parser.parse_args()
    schoolID=args.id
    paint(schoolID)