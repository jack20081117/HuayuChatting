from tools import *

with open('../out/chattingAllTime.txt','r') as reader:
    chattingAllTime=json.load(reader)
with open('../out/chattingSTTime.txt','r') as reader:
    chattingSTTime=json.load(reader)

def require(sTime,tTime,*args):
    length=len(args)
    schoolIDs:list[str]=[]
    #probabilities:list[float]=[]
    s2pDict:dict[str,float]={}
    for id in range(0,length,2):
        schoolID=args[id]
        probability=args[id+1]
        schoolIDs.append(schoolID)
        s2pDict[schoolID]=probability
    situations=0
    parts=len(chattingAllTime)
    for partId in range(parts):
        if sTime!=-1 or tTime!=-1:
            if chattingSTTime[0][partId]<sTime or chattingSTTime[1][partId]>tTime:
                continue
        correct=True
        chattingEachPart=chattingAllTime[partId]
        partlength=len(chattingEachPart)
        if partlength<=10:continue
        s2fDict:dict[str,int]={}
        for schoolID in chattingEachPart:
            if schoolID=='other':continue
            if not schoolID in s2fDict:s2fDict[schoolID]=0
            s2fDict[schoolID]+=1
        for schoolID in s2pDict:
            if not schoolID in s2fDict:correct=False;break
            if s2fDict[schoolID]/partlength<=s2pDict[schoolID]:correct=False;break
        if correct:
            #print(chattingEachPart)
            situations+=1
            print('此片段开始时间:%s'%chattingSTTime[0][partId])
            print('此片段结束时间:%s'%chattingSTTime[1][partId])
            print('此片段共%d句话'%partlength)
            for schoolID in schoolIDs:
                print('学号:%s,片段中发言次数:%s,占比:%.5f'%
                      (schoolID,s2fDict[schoolID],s2fDict[schoolID]/partlength))
            print('')
    print('共%d个片段满足要求\n'%situations)

if __name__ == '__main__':
    #print(len(chattingAllTime))
    while True:
        try:
            studentnum=int(input('请输入您想了解的片段中有具体要求的学生个数:'))
            arguments=[]
            for i in range(studentnum):
                schoolID=input('请输入您想了解片段中有具体要求的的学生学号:')
                probability=float(input('请输入您希望这位学生的发言所占比率(0~1):'))
                arguments.append(schoolID)
                arguments.append(probability)
            ifLimited=input('是否需要限制发言片段的起止时间?y/n')
            if ifLimited=='y':
                print('请输入起止时间:(格式:YYYY-MM-DD hh:mm:ss)')
                sTime=input('开始时间:')
                tTime=input('结束时间:')
                require(sTime,tTime,*arguments)
            elif ifLimited=='n':
                require(-1,-1,*arguments)
            else:
                print('输入错误,默认不进行限制')
                require(-1,-1*arguments)
        except Exception as e:
            print('遇到错误:%s'%e)
            print('请重新输入!')