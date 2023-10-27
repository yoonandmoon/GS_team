# !pip install mecab-ko-msvc mecab-ko-dic-msvc
# 코랩에서 진행 시

import warnings
import pandas as pd
import MeCab
import re
from collections import Counter

warnings.filterwarnings(action = 'ignore')

# csv파일 불러오기
df = pd.read_csv("C:\\DA\\GSTEAM\\GS_team\\01pretreatment\\csv\\news\\raw_data\\R_gs_news2211.csv")

# df2에 필요정보만 저장
df2 = df[['date','title','content']]

# 타이틀, 콘텐트 \n, \t,\r 제거
# 데이트 날짜만 분리
df2['date'] = df['date'].str.split(' ').str[0]
df2['title'] = df['title'].str.replace('\n',' ').replace('\t',' ').replace('\r', ' ')
df2['content'] = df['content'].str.replace('\n',' ').replace('\t',' ').replace('\r', ' ')

# 토큰화
#Mecab 인스턴스 생성
m = MeCab.Tagger()

# 한글 문자만 남기고 나머지 문자 제거 후 새 열에 저장
df2['Title'] = df2['title'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', '', x))
df2['Content'] = df2['content'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', '', x))

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
                pos = pos.split(',')[0]  # 품사 정보에서 첫 번째 부분 사용

                # 선택 조건 (명사, 동사, 형용사)을 확인 후 선택된 단어 리스트에 추가
                if len(word) >= 2 and pos in ['NNG', 'VV', 'VA']:
                    selected_words.append(word)

    # 선택된 단어를 공백으로 구분된 문자열로 반환
    return ' '.join(selected_words)

# 'title' 및 'content' 열에 대해 처리
for i, row in df2.iterrows():
    df2.at[i, 'Title'] = extract_words(row['title'])
    df2.at[i, 'Content'] = extract_words(row['content'])

df3 = df2[['date','Title','Content']]

# 불용어 처리
# 제목은 처리 안함
# 단어 빈도수 오름차순 정리
# 불용어 리스트 작성
Cwords_list = df3['Content'].str.split()
all_Cwords = [word for words in Cwords_list for word in words]
Cword_counts = Counter(all_Cwords)
most_common_Cwords = Cword_counts.most_common(500)

print("제목에서 가장 많이 나온 상위 50개 단어:")
for word, count in most_common_Cwords:
    print(f"{word}: {count}")

stop_Cword = ['건설','건설사','올해','최근','이번','상황','가운데','활용','이후','지난해','관련']

def preprocess(text):
  text = text.split()
  text = [i for i in text if i not in stop_Cword]
  return text

def make_tokens(df):
  df['tokens'] = ' '
  for i, row in df.iterrows():
    if i%100==0:
      print(i,'/',len(df))
    token = preprocess(df['Content'][i])
    df['tokens'][i] = ' '.join(token)
  return df

DF = make_tokens(df3)
print(DF)
DF.to_csv('gs_news2212(ver.C01).csv', index = False)