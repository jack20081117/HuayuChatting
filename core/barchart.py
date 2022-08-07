import numpy
from tools import *
from matplotlib import pyplot

info=readInfoByJson()
schoolID2qq,schoolID2freq,schoolID2days,schoolID2rate=info[0:4]
schoolIDs=[]
qqs=[]
freqs:list[list]=[[],[],[],[]]
schoolIDs_freq:list[list]=[[],[],[],[]]

rates:list[list]=[[],[],[]]
schoolIDs_rate:list[list]=[[],[],[]]

for schoolID,qq in schoolID2qq.items():
    schoolIDs.append(schoolID)
    qqs.append(schoolID)
for schoolID in schoolIDs:
    freq=schoolID2freq[schoolID]
    if freq>10000:
        freqs[0].append(freq)
        schoolIDs_freq[0].append(schoolID)
    elif freq>5000:
        freqs[1].append(freq)
        schoolIDs_freq[1].append(schoolID)
    elif freq>2000:
        freqs[2].append(freq)
        schoolIDs_freq[2].append(schoolID)
    else:
        freqs[3].append(freq)
        schoolIDs_freq[3].append(schoolID)

for schoolID in schoolIDs:
    rate=schoolID2rate[schoolID]
    if rate>100:
        rates[0].append(rate)
        schoolIDs_rate[0].append(schoolID)
    elif rate>50:
        rates[1].append(rate)
        schoolIDs_rate[1].append(schoolID)
    else:
        rates[2].append(rate)
        schoolIDs_rate[2].append(schoolID)

def paint():
    x=numpy.array(schoolIDs_freq[0])
    y=numpy.array(freqs[0])
    pyplot.bar(x,y)
    pyplot.xlabel('Students who spoke over 10000 times')
    pyplot.ylabel('The accurate number of messages')
    pyplot.title('Frequency')
    pyplot.show()

    x=numpy.array(schoolIDs_freq[1])
    y=numpy.array(freqs[1])
    pyplot.bar(x,y)
    pyplot.xlabel('Students who spoke over 5000 times')
    pyplot.ylabel('The accurate number of messages')
    pyplot.title('Frequency')
    pyplot.show()

    x=numpy.array(schoolIDs_freq[2])
    y=numpy.array(freqs[2])
    pyplot.bar(x,y)
    pyplot.xlabel('Students who spoke over 2000 times')
    pyplot.ylabel('The accurate number of messages')
    pyplot.title('Frequency')
    pyplot.show()

    x=numpy.array(schoolIDs_rate[0])
    y=numpy.array(rates[0])
    pyplot.bar(x,y)
    pyplot.xlabel('Students who spoke over 100 times every day')
    pyplot.ylabel('The accurate number of messages')
    pyplot.title('Rate')
    pyplot.show()

    x=numpy.array(schoolIDs_rate[1])
    y=numpy.array(rates[1])
    pyplot.bar(x,y)
    pyplot.xlabel('Students who spoke over 50 times every day')
    pyplot.ylabel('The accurate number of messages')
    pyplot.title('Rate')
    pyplot.show()

if __name__ == '__main__':
    paint()