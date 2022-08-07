import xlwt

HuayuVote=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=HuayuVote.add_sheet('华育校友营投票',cell_overwrite_ok=True)

with open('../in/votecount.txt') as reader:
    text=reader.readlines()

candidateID=0
voterID=0
voters={}

for rawLine in text:
    line=rawLine[0:-1]
    #print(line)
    demand=line[0:5]
    if demand=='Enter':
        #print(line)
        lineType=line[-1]
        if lineType=='t':
            continue
        lineType=line[-7]
        if lineType=='e':
            candidateID+=1
            schoolID=line[-5:]
            sheet.write(0,candidateID,schoolID)
        else:
            schoolID=line[-5:]
            if schoolID in voters:
                voter=voters[schoolID]
                sheet.write(voter,candidateID,1)
            else:
                votersNum=len(voters)
                voters[schoolID]=votersNum+1
                sheet.write(votersNum+1,0,schoolID)
                sheet.write(votersNum+1,candidateID,1)
    else:
        #print(line)
        continue

HuayuVote.save('../out/华育投票.xls')

if __name__ == '__main__':
    pass