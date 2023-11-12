import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import *

dataframe=pd.read_excel('../out/华育校友营周发言比率.xls',sheet_name='华育校友营',index_col=0)

dataframe=dataframe.transpose()
dataframe.fillna(0,inplace=True)

data={}

for weekKey in dataframe.index:
    sum=0
    weekframe=dataframe.loc[weekKey]
    for p in weekframe:
        if p:
            sum+=-p*np.log2(p)
    weekKey=str(weekKey)[:10]
    data[weekKey]=sum

def paint():
    xs,raw_ys,ys=[],[],[]
    for key,value in data.items():
        xs.append(datetime.strptime(key,'%Y-%m-%d').date())
        raw_ys.append(value)
        ys.append(0)
    for i in range(len(raw_ys)):
        if i==0:
            ys[i]=(raw_ys[i]+raw_ys[i+1])/2
        elif i==len(raw_ys)-1:
            ys[i]=(raw_ys[i]+raw_ys[i-1])/2
        else:
            ys[i]=(raw_ys[i-1]+raw_ys[i]+raw_ys[i+1])/3
    plt.plot_date(xs,ys,linestyle='-',marker=',',label='average')
    plt.plot_date(xs,raw_ys,linestyle='--',marker='.',alpha=0.5,c='green',label='raw')
    plt.legend()
    plt.title('Entropy chart')
    plt.show()

if __name__ == '__main__':
    paint()