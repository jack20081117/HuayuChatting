import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import xlwt

with open('hyctVec.vector','r') as f:
    data=f.readlines()

dataStr=data[1:]
#dataStr=dataStr[:80]
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

HuayuChatting=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=HuayuChatting.add_sheet('华育校友营',cell_overwrite_ok=True)

col=('schoolID','x','y')
for i in range(3):
    sheet.write(0,i,col[i])

length=len(schoolIDs)
for i in range(length):
    sheet.write(i+1,0,schoolIDs[i])
    sheet.write(i+1,1,float(xs[i]))
    sheet.write(i+1,2,float(ys[i]))

HuayuChatting.save('../out/华育校友营降维数据.xls')
for i in range(length):
    plt.text(xs[i],ys[i],schoolIDs[i],fontsize=8)
plt.scatter(xs,ys,s=10,marker='D')
plt.grid()
plt.show()

if __name__ == '__main__':
    pass