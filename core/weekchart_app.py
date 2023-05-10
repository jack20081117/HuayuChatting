from tools import *
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot
from datetime import *
from argparse import ArgumentParser

with open('../out/chattingAllWeeks.txt','r') as reader:
    chattingAllWeeks=json.load(reader)
schoolID2weeks={}
schoolIDs=set()

for weekKey in chattingAllWeeks:
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
        if schoolID=='robot': continue
        schoolIDs.add(schoolID)
        if not schoolID in schoolID2weeks: schoolID2weeks[schoolID]={}

for schoolID in schoolIDs:
    for weekKey in chattingAllWeeks:
        if not weekKey in schoolID2weeks[schoolID]:
            schoolID2weeks[schoolID][weekKey]=0

for weekKey in chattingAllWeeks:
    weekValue=chattingAllWeeks[weekKey]
    for schoolID in weekValue:
        if schoolID=='robot': continue
        schoolID2weeks[schoolID][weekKey]+=1


def paint(schoolID):
    data=schoolID2weeks[schoolID]
    xs,ys=[],[]
    for key,value in data.items():
        xs.append(datetime.strptime(key[0:10],'%Y-%m-%d').date())
        ys.append(value)
    pyplot.figure(figsize=(10,5))
    pyplot.plot_date(xs,ys,linestyle='-',marker='.')
    pyplot.title(schoolID)
    pyplot.savefig("./static/img/weekchart.png")

if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument(
        "--id",
        help="Insert the SchoolID you want to know",
        dest="id",default=None)
    args=parser.parse_args()
    schoolID=args.id
    paint(schoolID)