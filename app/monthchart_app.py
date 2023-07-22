import numpy
from tools import *
from matplotlib import pyplot
from datetime import *
from argparse import ArgumentParser

with open('../out/chattingAllMonths.txt','r') as reader:
    chattingAllMonths=json.load(reader)
schoolID2months={}
schoolIDs=set()

for monthKey in chattingAllMonths:
    monthValue=chattingAllMonths[monthKey]
    for schoolID in monthValue:
        if schoolID=='robot':continue
        schoolIDs.add(schoolID)
        if not schoolID in schoolID2months:schoolID2months[schoolID]={}

for schoolID in schoolIDs:
    for monthKey in chattingAllMonths:
        if not monthKey in schoolID2months[schoolID]:
            schoolID2months[schoolID][monthKey]=0

for monthKey in chattingAllMonths:
    monthValue=chattingAllMonths[monthKey]
    for schoolID in monthValue:
        if schoolID=='robot':continue
        schoolID2months[schoolID][monthKey]+=1

def paint(schoolID):
    data=schoolID2months[schoolID]
    xs,ys=[],[]
    for key,value in data.items():
        xs.append(datetime.strptime(key,'%Y-%m').date())
        ys.append(value)
    pyplot.figure(figsize=(10,5))
    pyplot.plot_date(xs,ys,linestyle='-',marker='.')
    pyplot.title(schoolID)
    pyplot.savefig("./static/img/monthchart.png")

if __name__ == '__main__':
    parser=ArgumentParser()
    parser.add_argument(
        "--id",
        help="Insert the SchoolID you want to know",
        dest="id",default=None)
    args=parser.parse_args()
    schoolID=args.id
    paint(schoolID)