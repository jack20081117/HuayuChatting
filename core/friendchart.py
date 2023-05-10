import json,xlwt

with open('../out/friendprobs_calc.txt','r') as reader:
    friendprobs_calc=json.load(reader)

HuayuFriends=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=HuayuFriends.add_sheet('华育校友营相似度',cell_overwrite_ok=True)

schoolIDs_part=[
    '20564','23212','21871','10361','14668',
    '20576','23208','21380','22369','23786',
    '22765','22885','22859','24367','22378',
    '22518','22205','22801','22868','22886',
    '23868','22888','23771','22371','22873',
    '23677','20851','21880','22555','20470',
    '21159','20352','21361','24885'
]
schoolIDs=[]
schoolID4num={}

for schoolID in friendprobs_calc:
    schoolIDs.append(schoolID)

length=len(schoolIDs)
partLength=len(schoolIDs_part)

for i in range(length):
    schoolID=schoolIDs[i]
    schoolID4num[i]=schoolID

for i in range(partLength):
    schoolID=schoolIDs_part[i]
    sheet.write(0,i+1,schoolID)

for i in range(length):
    schoolID=schoolID4num[i]
    sheet.write(i+1,0,schoolID)

for i in range(partLength):
    for j in range(length):
        if not schoolID4num[j] in friendprobs_calc[schoolIDs_part[i]]:
            friendprobs_calc[schoolIDs_part[i]][schoolID4num[j]]=0
        sheet.write(j+1,i+1,friendprobs_calc[schoolIDs_part[i]][schoolID4num[j]])

HuayuFriends.save('../out/华育校友营相似度.xls')

if __name__=='__main__':
    pass
