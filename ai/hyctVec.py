from gensim.models import Word2Vec

import json,multiprocessing

with open('../out/chattingAllTime.txt','r') as reader:
    chattingAllTime=json.load(reader)

model=Word2Vec(sentences=chattingAllTime,vector_size=32,min_count=1,workers=multiprocessing.cpu_count())

print("Saved model:",model)

model.save('hyctVec.model')
model.wv.save_word2vec_format('hyctVec.vector')