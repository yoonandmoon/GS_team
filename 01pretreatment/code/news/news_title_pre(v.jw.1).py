import warnings
import pandas as pd
import MeCab
import re
from collections import Counter

warnings.filterwarnings(action = 'ignore')

# csv파일 불러오기
df = pd.read_csv("C:\\DA\\GSTEAM\\GS_team\\news_combined(v.1.jw).csv")
df2 = df[['Title','Content']]
df2 = df2.dropna(subset=['Title'])

#불용어리스트
Twords_list = df2['Title'].str.split()
all_Cwords = [word for words in Twords_list for word in words]
Tword_counts = Counter(all_Cwords)
most_common_Twords = Tword_counts.most_common(1000)

print("제목에서 가장 많이 나온 상위 1000개 단어:")
for word, count in most_common_Twords:
    print(f"{word}: {count}")