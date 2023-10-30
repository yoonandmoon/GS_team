import warnings
warnings.filterwarnings(action = 'ignore')
import pandas as pd
df = pd.read_csv('C:/Users/rhksa/OneDrive/바탕 화면/gs project/GS_team/01pretreatment/csv/news/gs_news2307(ver.C01).csv')

from gensim import corpora
from gensim.models import LdaModel, TfidfModel

tokenized_docs = df['contentToken'].apply(lambda x: x.split())
id2word = corpora.Dictionary(tokenized_docs)
corpus_TDM =[id2word.doc2bow(doc) for doc in tokenized_docs]
tfidf =  TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]
n = 10
lda = LdaModel(corpus=corpus_TFIDF,
               id2word=id2word,
               num_topics=n,
               random_state=100)

for t in lda.print_topics() :
  print(t)

import pyLDAvis
import pyLDAvis.gensim
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda, corpus_TFIDF, id2word)
pyLDAvis.display(vis)

