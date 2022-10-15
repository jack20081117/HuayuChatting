from tools import *
from matplotlib import pyplot
import numpy,json,random

info=readInfoByJson()
chattingAllTime=info[4]

friends:dict[str,dict[str,int]]={}
friendprobs:dict[str,dict[str,float]]={}
friendprobs_calc:dict[str,dict[str,float]]={}

parts=len(chattingAllTime)

for partId in range(parts):
    chattingEachPart=chattingAllTime[partId]
    considered=[]
    for schoolID in chattingEachPart:
        if schoolID in considered or schoolID=='robot':continue
        considered.append(schoolID)
        for otherID in chattingEachPart:
            if otherID==schoolID or otherID=='robot':continue
            if not schoolID in friends:friends[schoolID]={}
            if not otherID in friends[schoolID]:friends[schoolID][otherID]=0
            friends[schoolID][otherID]+=1

for schoolID in friends:
    schoolIDFriends=friends[schoolID]
    friendsum=sumOfValue(schoolIDFriends)
    friendprobs[schoolID]={}
    for otherID in schoolIDFriends:
        friendnum=schoolIDFriends[otherID]
        friendprobs[schoolID][otherID]=friendnum/friendsum

for schoolID in friends:
    schoolIDFriends=friends[schoolID]
    friendprobs_calc[schoolID]={}
    for otherID in schoolIDFriends:
        friendprobs_calc[schoolID][otherID]=1-(1-friendprobs[schoolID][otherID])*(1-friendprobs[otherID][schoolID])

with open('../out/friendprobs_calc.txt','w') as writer:
    json.dump(friendprobs_calc,writer)

if __name__ == '__main__':
    ifPie=input('是否展示饼图?y/n')
    if ifPie=='y':ifShow=True
    elif ifPie=='n':ifShow=False
    else:
        print('输入错误,默认不展示饼图')
        ifShow=False
    while True:
        try:
            schoolID=input('请输入您想了解的学号:')
            schoolIDFriends=friends[schoolID]
            schoolIDFriendsSorted=sortByValue(schoolIDFriends)
            friendsum=sumOfValue(schoolIDFriends)
            number=0
            print('以下是和该学号最亲近的五个人的学号:')
            pieList:list=[]
            pieFriendList:list=[]
            gameList:list=[]
            for t in schoolIDFriendsSorted:
                friendID=t[0]
                friendnum=t[1]
                friendprob=friendnum*100/friendsum
                pieList.append(friendprob)
                pieFriendList.append(friendID)
                if number<5:
                    print('学号:%s,邻接条数:%s条,在所有邻接记录中的占比:%.5f%%'%(friendID,friendnum,friendprob))
                if number<15:
                    gameList.append(friendID)
                number+=1
            pieArray=numpy.array(pieList)
            pyplot.pie(pieArray,labels=pieFriendList,labeldistance=0.5,radius=1.2,rotatelabels=True)
            pyplot.title('The friends of %s'%schoolID)

            random.shuffle(gameList)
            print('随机抽取好友:%s'%','.join(gameList[:5]))
            if ifShow:
                pyplot.show()
        except KeyError as e:
            print('输入错误，请重新输入！')