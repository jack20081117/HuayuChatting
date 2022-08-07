import numpy
from matplotlib import pyplot
from tools import *

info=readInfoByJson()
timeDeltas=info[8]
chattingAllDeltas=info[9]

def paint1():
    xs=[]
    ys=[]
    timeDeltaID=0
    for timeDelta in timeDeltas:
        timeDeltaID+=1
        xs.append(timeDeltaID)
        ys.append(timeDelta)
    NPxs=numpy.array(xs)
    NPys=numpy.array(ys)
    pyplot.plot(NPxs,NPys)
    pyplot.show()
    sortedTimeDeltas=sorted(timeDeltas,key=lambda delta:delta,reverse=True)
    sortedNPys=numpy.array(sortedTimeDeltas)
    pyplot.plot(NPxs,sortedNPys)
    pyplot.show()

def paint2():
    xs=[]
    ys=[]
    sortedChattingDeltas=sorted(chattingAllDeltas.items(),key=lambda t:t[0],reverse=True)
    for t in sortedChattingDeltas:
        xs.append(int(t[0]))
        ys.append(int(t[1]))
    NPxs=numpy.array(xs)
    NPys=numpy.array(ys)
    pyplot.bar(NPxs,NPys)
    pyplot.show()

if __name__ == '__main__':
    #paint1()
    paint2()