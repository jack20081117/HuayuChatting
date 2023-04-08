from matplotlib import pyplot
from datetime import *
from tools import *
from argparse import ArgumentParser

with open('../out/chattingAllWeeks.txt','r') as reader:
    chattingAllWeeks=json.load(reader)
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

def paint(schoolID):
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
    pyplot.figure(figsize=(10,5))
    pyplot.plot_date(xs,ys,linestyle='-',marker='.')
    pyplot.title(schoolID)
    pyplot.savefig("./static/img/decaychart.png")

if __name__ == '__main__':
    parser=ArgumentParser()
    parser.add_argument(
        "--id",
        help="Insert the SchoolID you want to know",
        dest="id",default=None)
    args=parser.parse_args()
    schoolID=args.id
    paint(schoolID)