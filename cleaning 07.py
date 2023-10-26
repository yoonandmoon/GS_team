import warnings
import pandas as pd
warnings.filterwarnings(action = 'ignore')

df = pd.read_csv("C:/Users/rhksa/OneDrive/바탕 화면/gs project/GS_team/news_data07.csv")

df2 = df[['title','content']]
df2['content'] = df['content'].str.replace('\n',' ').replace('\t',' ').replace('\r', ' ')

from konlpy.tag import Komoran
import re
tokenizer = Komoran()

df2['morphs'] = None
for i, row in df.iterrows():
    df2['morphs'][i] = ' '.join(tokenizer.morphs(row['content']))

# 한글 문자만 남기고 나머지 문자 제거
df2['morphs'] = df2['morphs'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', '', x))

import spacy

# spaCy의 NLP 모델을 로드합니다.
nlp = spacy.load('en_core_web_sm')

def extract_words(text):
    # 텍스트를 spaCy의 NLP 모델을 사용하여 토큰화합니다.
    doc = nlp(text)
      
    # 길이가 2글자 이상이고, 명사(Noun), 동사(Verb), 형용사(Adjective)인 단어를 선택합니다.
    selected_words = [token.text for token in doc if len(token.text) >= 2 and token.pos_ in ['NOUN', 'VERB', 'ADJ']]
      
    # 선택된 단어를 공백으로 구분된 문자열로 결합합니다.
    return ' '.join(selected_words)

df2['morphs'] = df2['morphs'].apply(extract_words)

df3 = df2[['title','morphs']]

stop_word = ['에서','ㄴ다','ㅂ니다','있다','으로','밝히']

def preprocess(text):
  text = text.split()
  text = [i for i in text if i not in stop_word]
  return text

def make_tokens(df):
  df['tokens'] = ' '
  for i, row in df.iterrows():
    if i%100==0:
      print(i,'/',len(df))
    token = preprocess(df['morphs'][i])
    df['tokens'][i] = ' '.join(token)
  return df

df4 = make_tokens(df3)
print(df4)

#불용어처리 확인
from collections import Counter

words_list = df4['tokens'].str.split()

all_words = [word for words in words_list for word in words]

word_counts = Counter(all_words)

most_common_words = word_counts.most_common(20)
print("가장 많이 나온 상위 20개 단어:")
for word, count in most_common_words:
    print(f"{word}: {count}")
