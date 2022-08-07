import xlwt
from tools import *

info=readInfoByJson()
schoolID2qq,schoolID2freq,schoolID2days,schoolID2rate=info[0:4]

HuayuChatting=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=HuayuChatting.add_sheet('华育校友营',cell_overwrite_ok=True)

qqList=dictValue2List(schoolID2qq)
freqList=dictValue2List(schoolID2freq)
rateList=dictValue2List(schoolID2rate)

schoolIDs=[]
for key,value in schoolID2qq.items():
    schoolIDs.append(key)

col=('schoolID','qq','freq','rate')
for i in range(4):
    sheet.write(0,i,col[i])

length=len(schoolID2qq)
for i in range(length):
    sheet.write(i+1,0,schoolIDs[i])
    sheet.write(i+1,1,qqList[i])
    sheet.write(i+1,2,freqList[i])
    sheet.write(i+1,3,rateList[i])

HuayuChatting.save('../out/华育校友营.xls')

if __name__ == '__main__':
    pass