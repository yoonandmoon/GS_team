# 불용어 처리
# 제목은 처리 안함
# 단어 빈도수 오름차순 정리
# 불용어 리스트 작성
Cwords_list = df3['Content'].str.split()
all_Cwords = [word for words in Cwords_list for word in words]
Cword_counts = Counter(all_Cwords)
most_common_Cwords = Cword_counts.most_common(1500)

print("제목에서 가장 많이 나온 상위 50개 단어:")
for word, count in most_common_Twords:
    print(f"{word}: {count}")

stop_Cword = ['건설','건설사',]

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

DF.to_csv('news06(ver.C01).csv', index = False)