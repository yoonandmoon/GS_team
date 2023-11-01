import warnings
warnings.filterwarnings(action = 'ignore')
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel, TfidfModel
import pyLDAvis
import pyLDAvis.gensim


df = pd.read_csv('C:\\DA\\GSTEAM\\GS_team\\01pretreatment\\stock_news_combine.csv')

tokenized_docs = df['Tokens_2'].apply(lambda x: x.split())
id2word = corpora.Dictionary(tokenized_docs)
corpus_TDM =[id2word.doc2bow(doc) for doc in tokenized_docs]
tfidf =  TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]
n = 15
lda = LdaModel(corpus=corpus_TFIDF,
               id2word=id2word,
               num_topics=n,
               random_state=100)

for t in lda.print_topics() :
  print(t)

vis = pyLDAvis.gensim.prepare(lda, corpus_TFIDF, id2word)
pyLDAvis.save_html(vis, 'lda(v.1).html')