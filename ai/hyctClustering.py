import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from hyctDecomposition import decomposition
plt.rcParams['font.family']=['Microsoft YaHei']

with open('hyctVec.vector','r') as f:
    data=f.readlines()

num=int(input('How many people do you want to show?'))

dataStr=data[1:]
dataStr=dataStr[:num]
embeddinglist=[]

for datumStr in dataStr:
    datumStr=datumStr[:-2]
    datumList=datumStr.split(' ')
    embeddinglist.append(datumList[1:])

embeddinglist=np.array(embeddinglist)

k=int(input('K:'))

kmeans=KMeans(n_clusters=k,random_state=0)
kmeans.fit(embeddinglist)

labels=np.array(kmeans.labels_)

nodePos,dataStr,schoolIDs=decomposition(num,'t')

xs,ys=[],[]

for i in range(len(dataStr)):
    xs.append(nodePos[i,0])
    ys.append(nodePos[i,1])

xs,ys=np.array(xs),np.array(ys)

for i in range(num):
    plt.text(xs[i],ys[i],schoolIDs[i],fontsize=8)

markers=['d','^','D','s','<','>','v','+']
colors=['blue','green','red','yellow','pink','purple','black','gray']

for i in range(k):
    plt.scatter(xs[labels==i],ys[labels==i],s=15,marker=markers[i],c=colors[i],label=str(i))

plt.legend()
plt.title('KMeans,num=%s,k=%s'%(num,k))
plt.grid()
plt.show()

if __name__ == '__main__':
    pass