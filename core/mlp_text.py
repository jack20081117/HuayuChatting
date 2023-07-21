import pandas as pd
import numpy as np
import jieba,re,json,socket,threading
import logging
logging.basicConfig(level=logging.INFO)
from datetime import datetime
from tqdm import tqdm
from extractor import searchQQ
from jieba import analyse
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,Activation,Flatten,MaxPool1D,Conv1D,Embedding,BatchNormalization
from matplotlib import pyplot as plt

ifLoadModel=True

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
    content=data_content[i]
    content=re.sub(r'\n','',content)
    content=re.sub(r'@\S+','',content)
    content=content.replace('[表情]','')
    content=content.replace('[图片]','')
    if len(content)<=5:
        continue
    dataframeJson.append(
        {
            "schoolID":schoolID,
            "content":content
        }
    )

dataframe=pd.DataFrame(dataframeJson)

#dataframe=dataframe.head(1000)

label=list(dataframe['schoolID'].unique())

def label_dataset(row):
    num_label=label.index(row)
    return num_label

dataframe['label']=dataframe['schoolID'].apply(label_dataset)

def keyWordExtract(texts):
    return ' '.join(analyse.extract_tags(texts,topK=20,withWeight=False,allowPOS=()))

dataframe['key_word']=dataframe['content'].apply(keyWordExtract)

token=Tokenizer(num_words=2000)
token.fit_on_texts(dataframe['key_word'])

text2seq=token.texts_to_sequences(dataframe['key_word'])
text2seq=tf.keras.preprocessing.sequence.pad_sequences(text2seq,maxlen=20)

x_train=text2seq
y_train=np.array(dataframe['label'].to_list())

maxLabel=max(dataframe['label'].to_list())
if not ifLoadModel:
    model=Sequential()
    model.add(Embedding(output_dim=32,input_dim=2000,input_length=20))
    model.add(Conv1D(256,3,padding='same',activation='relu'))
    model.add(MaxPool1D(3,3,padding='same'))
    model.add(Conv1D(32,3,padding='same',activation='relu'))
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=maxLabel+1,activation='softmax'))

    batchSize=256
    epochs=15

    model.summary()
    model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

    history=model.fit(
        x=x_train,
        y=y_train,
        batch_size=batchSize,
        epochs=epochs,
        validation_split=0.2
    )

    model.save('mlp_text.h5')

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
    model=load_model("mlp_text.h5")

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('127.0.0.1',9999))

useBot=True

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
        l=list(model.predict(sequence)[0])
        num=l.index(max(l))
        schoolID=dataframe[dataframe.label==num]["schoolID"].to_list()[0]
        if max(l)>0.1:
            print('schoolID:%s,confidence:%.5f'%(schoolID,max(l)))
        else:
            print('抱歉，无法找到匹配的发言者')