import requests
from datetime import datetime
from sql import *
import sqlite3
import random
import os,json
from bs4 import BeautifulSoup

group_ids=[734894275,719772033]
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'}

with open('../out/qq2schoolID.txt','r') as reader:
    qq2schoolID=json.load(reader)

def getWeather():
    res=requests.get('http://www.weather.com.cn/weather15d/101020100.shtml')
    res.encoding='utf-8'
    html=res.text
    soup=BeautifulSoup(html,'html.parser')  #解析文档
    weathers=soup.find(id="15d",class_="c15d").find('ul',class_="t clearfix").find_all('li')
    results=[]
    for weather in weathers:
        weather_date=weather.find('span',class_="time")
        weather_wea=weather.find('span',class_="wea")
        weather_tem=weather.find('span',class_="tem")
        weather_wind=weather.find('span',class_="wind")
        weather_wind1=weather.find('span',class_="wind1")
        result='日期：'+weather_date.text+'天气：'+weather_wea.text+'温度：'+weather_tem.text+'风力：'+weather_wind.text+weather_wind1.text
        results.append(str(result))
    return results

def handle(res,group):
    ans=''
    if group:
        message=res.get("raw_message")
        uid=res.get('sender').get('user_id')
        gid=res.get('group_id')
        if gid not in group_ids:
            return None
        if "[CQ:at,qq=2470751924]" in message:
            message_list=message.split(' ')
            func_str=message_list[1]
            if func_str=='time':
                ans='当前时间为：%s'%datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elif func_str=='插入数据':
                if len(message_list)!=5:
                    send(gid,'数据必须以主语 谓语 宾语形式进行插入！',group=True)
                    return None
                subject,verb,object=message_list[2:]
                with sqlite3.connect('text.db') as conn:
                    cursor=conn.cursor()
                    cursor.execute('select * from sentence')
                    sentences=cursor.fetchall()
                    id=sentences[-1][0]+1 if sentences else 1
                    cursor.execute(insertText%(id,subject,verb,object))
                    ans='插入数据成功！'
            elif func_str=='查询数据':
                if len(message_list)<=3:
                    send(gid,'请以正确方式查询数据！',group=True)
                    return None
                sub_func_str=message_list[2]
                if sub_func_str=='id':
                    id=message_list[3]
                    with sqlite3.connect('text.db') as conn:
                        cursor=conn.cursor()
                        cursor.execute(selectByID,(id,))
                        value=cursor.fetchall()
                        if value:
                            ans='ID为%s的数据是：'%id+'-'.join(value[0][1:])
                        else:
                            ans='抱歉，没有找到ID为%s的数据'%id
            elif func_str=='抽卡':
                num=random.randint(1,5)
                if num>1:
                    ans='很遗憾，抽卡失败！'
                else:
                    num=random.randint(1,2)
                    if num==1:
                        ans='恭喜抽中卡牌：好运卡'
                    else:
                        ans='恭喜抽中卡牌：学霸卡'
            elif func_str=='添加问答':
                if len(message_list)!=4:
                    send(gid,'请按照合适格式进行添加问答！',group=True)
                    return None
                question,answer=message_list[2:]
                with sqlite3.connect('text.db') as conn:
                    cursor=conn.cursor()
                    cursor.execute(insertQA%(question,answer))
                    ans="插入问答成功！"
            elif func_str=='今日人品':
                num=random.randint(1,100)
                if num<=20:
                    ans='真糟糕，你今天的人品值只有%d！做了什么亏心事？'%num
                elif num<=40:
                    ans='很遗憾，你今天的人品值只有%d。快点攒攒人品吧！'%num
                elif num<=60:
                    ans='哎呀，你今天的人品值为%d。要继续努力呀！'%num
                elif num<=80:
                    ans='嗯，你今天的人品值为%d。还有上升空间！'%num
                elif num<=99:
                    ans='很不错，你今天的人品值为%d。请继续保持哦！'%num
                else:
                    ans='天哪！你今天的人品值是100！100！100！恭喜！'
            elif func_str=='天气' or func_str=='weather':
                results=getWeather()
                ans='上海近一周天气情况：\n'
                ans+='\n'.join(results)
            elif func_str=='weekchart':
                if len(message_list)!=3:
                    send(gid,'请以正确方式查询weekchart！',group=True)
                    return None
                schoolID=message_list[2]
                if schoolID not in qq2schoolID.values():
                    send(gid,'抱歉，查无此人！',group=True)
                    return None
                os.system('python weekchart_app.py --id %s'%schoolID)
                ans='[CQ:image,file=weekchart.png]'
            elif func_str=='help' or func_str=='帮助':
                ans='您好！欢迎使用森bot！\n'
                ans+='您可以使用如下功能：\n'
                ans+='1:查询时间：输入 time\n'
                ans+='2:插入数据：输入 插入数据 `主语` `谓语` `宾语`\n'
                ans+='3:查询数据：输入 查询数据 `编号` `id`来查询编号为id的数据\n'
                ans+='4.1:添加问答：输入 添加问答 `问题` `答案`\n'
                ans+='4.2:问问题：输入 `问题`来得到答案\n'
                ans+='5.1:Weekchart：输入 weekchart `学号`来得到该人的weekchart'
            else:
                answers=[]
                with sqlite3.connect('text.db') as conn:
                    cursor=conn.cursor()
                    cursor.execute(selectQA,(func_str,))
                    replies=cursor.fetchall()
                    for reply in replies:
                        if func_str==reply[0]:
                            answers.append(reply[1])
                if not answers:
                    ans='对不起，森bot没听懂您在说什么呢~'
                else:
                    if len(answers)==1:
                        ans=answers[0]
                    else:
                        ans='对于这个问题，我有%d个回答：\n'%len(answers)
                        for i in range(len(answers)):
                            answer=answers[i]
                            ans+='No.%d:%s\n'%(i+1,answer)
            send(gid,'[CQ:at,qq=%s]'%uid+ans,group=True)
    else:
        message=res.get("raw_message")
        uid=res.get('sender').get('user_id')
        message_list=message.split(' ')
        func_str=message_list[0]
        if func_str=='time':
            ans='当前时间为：%s'%datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif func_str=='插入数据':
            if len(message_list)!=4:
                send(uid,'数据必须以主语 谓语 宾语形式进行插入！',group=False)
                return None
            subject,verb,object=message_list[1:]
            with sqlite3.connect('text.db') as conn:
                cursor=conn.cursor()
                cursor.execute('select * from sentence')
                sentences=cursor.fetchall()
                id=sentences[-1][0]+1 if sentences else 1
                cursor.execute(insertText%(id,subject,verb,object))
                ans='插入数据成功！'
        elif func_str=='查询数据':
            if len(message_list)<=2:
                send(uid,'请以正确方式查询数据！',group=False)
                return None
            sub_func_str=message_list[1]
            if sub_func_str=='id':
                id=message_list[2]
                with sqlite3.connect('text.db') as conn:
                    cursor=conn.cursor()
                    cursor.execute(selectByID,(id,))
                    value=cursor.fetchall()
                    if value:
                        ans='ID为%s的数据是：'%id+'-'.join(value[0][1:])
                    else:
                        ans='抱歉，没有找到ID为%s的数据'%id
        elif func_str=='添加问答':
            if len(message_list)!=4:
                send(uid,'请按照合适格式进行添加问答！',group=False)
                return None
            question,answer=message_list[2:]
            with sqlite3.connect('text.db') as conn:
                cursor=conn.cursor()
                cursor.execute(insertQA%(question,answer))
                ans="插入问答成功！"
        elif func_str=='help' or func_str=='帮助':
            ans='您好！欢迎使用森bot！\n'
            ans+='您可以使用如下功能：\n'
            ans+='1:查询时间：输入 time\n'
            ans+='2:插入数据：输入 插入数据 `主语` `谓语` `宾语`\n'
            ans+='3:查询数据：输入 查询数据 `编号` `id`来查询编号为id的数据\n'
            ans+='4.1:添加问答：输入 添加问答 `问题` `答案`\n'
            ans+='4.2:问问题：输入 `问题`来得到答案'
        else:
            answers=[]
            with sqlite3.connect('text.db') as conn:
                cursor=conn.cursor()
                cursor.execute(selectQA,(func_str,))
                replies=cursor.fetchall()
                for reply in replies:
                    if func_str==reply[0]:
                        answers.append(reply[1])
            if not answers:
                ans='对不起，森bot没听懂您在说什么呢~'
            else:
                if len(answers)==1:
                    ans=answers[0]
                else:
                    ans='对于这个问题，我有%d个回答：\n'%len(answers)
                    for i in range(len(answers)):
                        answer=answers[i]
                        ans+='No.%d:%s\n'%(i+1,answer)
        send(uid,ans,group=False)

def send(id,message,group=False):
    """
    用于发送消息的函数
    :param uid: 用户id
    :param message: 发送的消息
    :param gid: 群id
    :return: none
    """

    if not group:
        # 如果发送的为私聊消息
        params={
            "user_id":id,
            "message":message,
        }
        resp=requests.get("http://127.0.0.1:5700/send_private_msg",params=params)
    else:
        params={
            'group_id':id,
            "message":message
        }
        resp=requests.get("http://127.0.0.1:5700/send_group_msg",params=params)