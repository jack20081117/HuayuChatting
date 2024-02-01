import pandas as pd
import numpy as np
import jieba,re,json,socket,threading
import logging
logging.basicConfig(level=logging.INFO)
from datetime import datetime
from tqdm import tqdm
from jieba import analyse
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,Activation,Flatten,MaxPool1D,Conv1D,Embedding,BatchNormalization,LSTM
from matplotlib import pyplot as plt

ifLoadModel=False
ifuseCNN=True
ifuseLSTM=False
ifShowAcc=False

def label_dataset(row):
    num_label=label.index(row)
    return num_label

def keyWordExtract(texts):
    return str(' '.join(analyse.extract_tags(texts,topK=20,withWeight=False,allowPOS=())))

def searchQQ(line):
    #寻找消息头中蕴含的qq号信息
    #由于可能有部分人在昵称中加入半角括号,所以从消息头末尾开始匹配
    #注意这里相反,是要先找下括号")"再找上括号"("
    #结尾别忘了把找到的qq号重新倒过来
    rline=line[::-1]
    rqq=re.search(r'(?<=[)>])[^(<]+',rline).group()
    return rqq[::-1]

filepath='../in/log.txt'
schoolIDpath='../out/qq2schoolID.txt'

with open(filepath,'r',encoding='utf-8',errors='ignore') as reader:
    txt: str=reader.read()

with open(schoolIDpath,'r',encoding='utf-8',errors='ignore') as reader:
    qq2schoolID=json.load(reader)

re_pat=r'20[\d-]{8}\s+[\d:]{7,8}\s+[^\n]+(?:\d{5,11}|@\w+\.[comnet]{2,3})[)>]'

data_head=re.findall(re_pat,txt)
data_content=re.split(re_pat,txt)[1:]

progress=tqdm(range(len(data_head)))

dataframeJson=[]

for i in progress:
    line=data_head[i]
    qq=searchQQ(line)  #发言者的qq号
    if qq not in qq2schoolID:
        continue
    schoolID=qq2schoolID[qq]
    if schoolID[:2]=='un':
        continue
    content=data_content[i]
    content=re.sub(r'\n','',content)
    content=re.sub(r'@\S+','',content)
    content=content.replace('[表情]','')
    content=content.replace('[图片]','')
    content=content.replace('[群签到]','')
    content=content.replace('请使用手机QQ进行查看。','')
    if len(content)<=10:
        continue
    dataframeJson.append(
        {
            "schoolID":schoolID,
            "content":content
        }
    )

dataframe=pd.DataFrame(dataframeJson)
label=list(dataframe['schoolID'].unique())
dataframe['label']=dataframe['schoolID'].apply(label_dataset)
dataframe['key_word']=dataframe['content'].apply(keyWordExtract)

#dataframe.to_csv("mlp_text.csv")

logging.info('Creating Tokenizer...')
token=Tokenizer(num_words=2000)
token.fit_on_texts(dataframe['key_word'])

text2seq=token.texts_to_sequences(dataframe['key_word'])
text2seq=tf.keras.preprocessing.sequence.pad_sequences(text2seq,maxlen=20)

x_train=np.array(text2seq,dtype=np.int16)
y_train=np.array(dataframe['label'].to_list(),dtype=np.int16)

test_size=int(len(x_train)*0.8)
x_test,y_test=x_train[test_size:],y_train[test_size:]

maxLabel=max(dataframe['label'].to_list())
if not ifLoadModel:
    if ifuseCNN:
        logging.info('Building CNN Model...')
        model=Sequential()
        model.add(Embedding(output_dim=32,input_dim=2000,input_length=20))
        model.add(Conv1D(256,3,padding='same',activation='relu'))
        model.add(MaxPool1D(3,3,padding='same'))
        model.add(Conv1D(128,3,padding='same',activation='relu'))
        model.add(MaxPool1D(3,3,padding='same'))
        model.add(Conv1D(32,3,padding='same',activation='relu'))
        model.add(Flatten())
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(units=256,activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(units=maxLabel+1,activation='softmax'))

        batchSize=256
        epochs=10

        model.summary()
        model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

        history=model.fit(
            x=x_train,
            y=y_train,
            batch_size=batchSize,
            epochs=epochs,
            validation_split=0.2
        )

        model.save('mlp_cnn.h5')
    elif ifuseLSTM:
        logging.info('Building LSTM Model...')
        model=Sequential()
        model.add(Embedding(output_dim=32,input_dim=2000,input_length=20))
        model.add(LSTM(units=256,return_sequences=True,input_dim=32,input_length=x_train.shape[1]))
        model.add(LSTM(units=32))
        model.add(Dense(units=256,activation='relu'))
        model.add(Dense(units=maxLabel+1,activation='softmax'))

        batchSize=256
        epochs=5

        model.summary()
        model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

        history=model.fit(
            x=x_train,
            y=y_train,
            batch_size=batchSize,
            epochs=epochs,
            validation_split=0.2
        )

        model.save('mlp_lstm.h5')
    else:
        raise Exception('You must choose a model!')

    if ifShowAcc:
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend(['Train','Valid'],loc='upper left')
        plt.show()

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(['Train','Valid'],loc='upper left')
        plt.show()
else:
    logging.info('Loading Model...')
    if ifuseCNN:
        model=load_model("mlp_cnn.h5")
    elif ifuseLSTM:
        model=load_model("mlp_lstm.h5")
    else:
        raise Exception("No model!")

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('127.0.0.1',9999))#通过TCP编程实现和机器人的通讯

useBot=False

def tcplink(sock,addr):
    logging.info('Accept new connection from %s:%s...'%addr)
    while True:
        data=sock.recv(10000)
        if not data or data.decode('utf-8')=='exit()':
            break
        sentence=data.decode('utf-8')
        sequence=token.texts_to_sequences([keyWordExtract(sentence)])
        sequence=tf.keras.preprocessing.sequence.pad_sequences(sequence,maxlen=20)
        l=list(model.predict(sequence)[0])
        num=l.index(max(l))
        schoolID=dataframe[dataframe.label==num]["schoolID"].to_list()[0]
        if max(l)>0.1:
            sock.send(('schoolID:%s,confidence:%.5f'%(schoolID,max(l))).encode('utf-8'))
        else:
            sock.send('抱歉，无法找到匹配的发言者'.encode('utf-8'))
    sock.close()
    logging.info('Connection from %s:%s closed.'%addr)

if useBot:
    s.listen(114514)
    logging.info('Waiting for connection......')
    while True:
        sock,addr=s.accept()
        # 创建新线程来处理TCP连接:
        t=threading.Thread(target=tcplink,args=(sock,addr))
        t.start()
else:
    while True:
        sentence=input('Sentence:')
        sequence=token.texts_to_sequences([keyWordExtract(sentence)])
        sequence=tf.keras.preprocessing.sequence.pad_sequences(sequence,maxlen=20)
        prediction=model.predict(sequence)
        l=list(prediction[0])
        num=l.index(max(l))
        schoolID=dataframe[dataframe.label==num]["schoolID"].to_list()[0]
        if max(l)>0.1:
            print('schoolID:%s,confidence:%.5f'%(schoolID,max(l)))
        else:
            print('抱歉，无法找到匹配的发言者')