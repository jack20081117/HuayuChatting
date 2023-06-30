from flask import Flask,request,redirect
import script

app=Flask(__name__)

@app.route('/',methods=['POST'])
def post():
    # 这里对消息进行分发，暂时先设置一个简单的分发
    res=request.get_json()
    if res.get('message_type')=='private':  # 说明有好友发送信息过来
        script.handle(res,group=False)
    elif res.get('message_type')=='group':
        script.handle(res,group=True)

    return 'OK'

if __name__=='__main__':
    app.run("127.0.0.1",port=5701,debug=True)  # 注意，这里的端口要和配置文件中的保持一致