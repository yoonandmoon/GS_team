import pandas as pd
df = pd.read_csv('C:\\DA\\GSTEAM\\GS_team\\01pretreatment\\csv\\news\\gs_news2309(ver.c01).csv')

from gensim import corpora
from gensim.models import LdaModel, TfidfModel

tokenized_docs = df['tokens'].apply(lambda x: x.split())
id2word = corpora.Dictionary(tokenized_docs)
corpus_TDM = [id2word.doc2bow(doc) for doc in tokenized_docs]
tfidf = TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]
n = 10
lda = LdaModel(corpus=corpus_TFIDF,
               id2word=id2word,
               num_topics=n,
               random_state=100)

for t in lda.print_topics():
    print(t)

import pyLDAvis
import pyLDAvis.gensim

vis = pyLDAvis.gensim.prepare(lda, corpus_TFIDF, id2word)
pyLDAvis.show(vis)  # 이 부분이 변경되었습니다.

# import pyLDAvis
# vis = pyLDAvis.gensim.prepare(lda, corpus_TFIDF, id2word)
# pyLDAvis.save_html(vis, 'lda.html')
# 웹서버로 부르는 버전, 'http://localhost:8000/lda.html#topic=0&lambda=1&term='