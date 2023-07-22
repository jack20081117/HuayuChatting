import json,logging

def dictKey2List(d):
    l=[]
    for key,value in d.items():
        l.append(key)
    return l

def dictValue2List(d):
    l=[]
    for key,value in d.items():
        l.append(value)
    return l

def sortByKey(d):
    #根据Key对Dict进行排序
    return sorted(d.items(),key=lambda t:t[0],reverse=True)

def sortByValue(d):
    #根据Value对Dict进行排序
    return sorted(d.items(),key=lambda t:t[1],reverse=True)

def sumOfValue(d):
    sum=0
    for key,value in d.items():
        sum+=value
    return sum

def transferList(l,src,target):
    for i in range(len(l)):
        item=l[i]
        if isinstance(item,list):
            l[i]=transferList(item,src,target)
        elif isinstance(item,str):
            if item==src:
                l[i]=target
    return l

def transferDict(d,src,target):
    for key,value in d.items():
        if isinstance(value,str):
            if value==src:
                d[key]=target
        if isinstance(value,dict):
            d[key]=transferDict(value,src,target)
        if isinstance(value,list):
            d[key]=transferList(value,src,target)
    return d