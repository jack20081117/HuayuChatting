import xlwt
from tools import *

with open('../out/qq2schoolID.txt','r') as reader:
    qq2schoolID=json.load(reader)
with open('../out/qq2freq.txt','r') as reader:
    qq2freq=json.load(reader)
with open('../out/qq2days.txt','r') as reader:
    qq2days=json.load(reader)
with open('../out/qq2rate.txt','r') as reader:
    qq2rate=json.load(reader)

HuayuChatting=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=HuayuChatting.add_sheet('华育校友营',cell_overwrite_ok=True)

schoolIDs=dictValue2List(qq2schoolID)
freqList=dictValue2List(qq2freq)
rateList=dictValue2List(qq2rate)
qqList=[]

for key,value in qq2schoolID.items():
    qqList.append(key)

col=('schoolID','qq','freq','rate')
for i in range(4):
    sheet.write(0,i,col[i])

length=len(qq2schoolID)
for i in range(length):
    sheet.write(i+1,0,schoolIDs[i])
    sheet.write(i+1,1,qqList[i])
    sheet.write(i+1,2,freqList[i])
    sheet.write(i+1,3,rateList[i])

HuayuChatting.save('../out/华育校友营.xls')

if __name__ == '__main__':
    pass