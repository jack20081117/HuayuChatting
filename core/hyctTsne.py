import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
plt.rcParams['font.family']=['Microsoft YaHei']

with open('hyctVec.vector','r') as f:
    data=f.readlines()

dataStr=data[1:]
dataStr=dataStr[:70]
embeddinglist=[]
schoolIDs=[]

for datumStr in dataStr:
    datumStr=datumStr[:-2]
    datumList=datumStr.split(' ')
    schoolIDs.append(datumList[0])
    embeddinglist.append(datumList[1:])

embeddinglist=np.array(embeddinglist)
down=TSNE(n_components=2,learning_rate=300,init='pca',perplexity=10)

nodePos=down.fit_transform(embeddinglist)

xs,ys=[],[]

for i in range(len(dataStr)):
    xs.append(nodePos[i,0])
    ys.append(nodePos[i,1])

length=len(schoolIDs)
for i in range(70):
    plt.text(xs[i],ys[i],schoolIDs[i],fontsize=8)

plt.scatter(xs[:5],ys[:5],s=10,marker='^',c='green',label='核心区')
plt.scatter(xs[5:15],ys[5:15],s=10,marker='D',c='red',label='相关区')
plt.scatter(xs[15:],ys[15:],s=10,marker='D',label='非相关区')
plt.legend()
plt.grid()
plt.show()

if __name__ == '__main__':
    pass