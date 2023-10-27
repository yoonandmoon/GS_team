import warnings
import pandas as pd
warnings.filterwarnings(action = 'ignore')

df = pd.read_csv('C:/Users/rhksa/OneDrive/바탕 화면/gs project/GS_team/News/Cleansing/news01(ver.R).csv')

df2 = df[['title','date','content']]
df2['content'] = df['content'].str.replace('\n',' ').replace('\t',' ').replace('\r', ' ')

import MeCab
import pandas as pd
import re

# Mecab 인스턴스 생성
m = MeCab.Tagger()

# 'title' 열의 결과를 'titl' 열에 저장
df2['Title'] = df2['title'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', ' ', x))

# 'content' 열의 결과를 'cont' 열에 저장
df2['Content'] = df2['content'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', ' ', x))

def extract_words(text):
    # 텍스트를 Mecab을 사용하여 토큰화합니다.
    tokens = m.parse(text).split('\n')

    # 선택된 단어를 저장할 리스트
    selected_words = []

    for token in tokens:
        if len(token) >= 2:
            # 각 토큰을 탭(\t)으로 분리하여 형태소와 품사 정보를 얻습니다.
            parts = token.split('\t')
            if len(parts) == 2:
                word, pos = parts
                pos = pos.split(',')[0]  # 품사 정보에서 첫 번째 부분만 사용

                # 선택 조건 (명사, 동사, 형용사)을 확인하고 선택된 단어 리스트에 추가
                if len(word) >= 2 and pos in ['NNG', 'VV', 'VA']:
                    selected_words.append(word)

    # 선택된 단어를 공백으로 구분된 문자열로 반환합니다.
    return ' '.join(selected_words)

# 'title' 및 'content' 열에 대해 처리
for i, row in df2.iterrows():
    df2.at[i, 'Title'] = extract_words(row['title'])
    df2.at[i, 'Content'] = extract_words(row['content'])

df3 = df2[['date','Title','Content']]

from collections import Counter

words_list = df3['Content'].str.split()

all_words = [word for words in words_list for word in words]

word_counts = Counter(all_words)

most_common_words = word_counts.most_common(50)
print("가장 많이 나온 상위 50개 단어:")
for word, count in most_common_words:
    print(f"{word}: {count}")


stop_word = ['기자','지난해','올해']

def preprocess(text):
  text = text.split()
  text = [i for i in text if i not in stop_word]
  return text

def preprocess(text):
  text = text.split()
  text = [i for i in text if i not in stop_word]
  return text

def make_tokens(df):
  df['tokens'] = ' '
  for i, row in df.iterrows():
    if i%100==0:
      print(i,'/',len(df))
    token = preprocess(df['Content'][i])
    df['tokens'][i] = ' '.join(token)
  return df

df4 = make_tokens(df3)

# 이후 불용어 확인 후 반복 이때는 불용어 처리시 이 코드 사용
#from collections import Counter

#words_list = df4['tokens'].str.split()

#all_words = [word for words in words_list for word in words]

#word_counts = Counter(all_words)

#most_common_words = word_counts.most_common(50)
#print("가장 많이 나온 상위 50개 단어:")
#for word, count in most_common_words:
    #print(f"{word}: {count}")

#날짜만 추출
df4['date'] = df4['date'].str.split(' ').str[0]

#결측값 제거
df4 = df4.dropna(subset=['tokens'])
print(df4)

#csv파일 만들기
df4.to_csv('news01(ver.C01).csv', index=False)
