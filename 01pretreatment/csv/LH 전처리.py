import warnings
import pandas as pd
import MeCab
import re
from collections import Counter

warnings.filterwarnings(action = 'ignore')

# csv파일 불러오기
df = pd.read_csv("C:\\Users\\rhksa\\OneDrive\\바탕 화면\\gs project\\GS_team\\01pretreatment\\csv\\news\\뉴스 데이터 2021-08 2023-10\\LH\\LH_2023-01-01_2023-10-31.csv")

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
# 'title' 열의 결과를 'titl' 열에 저장
df2['titl'] = df2['title'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', ' ', str(x)))
# 'content' 열의 결과를 'cont' 열에 저장
df2['cont'] = df2['content'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', ' ', str(x)))


def extract_words(text):
    text = str(text)
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


# 불용어 사전 만들고 나서 진행하기
stop_Cword = ['전용', '단지', '구역', '가능', '올해', '면적', '관계자', '따르', '국제', '브랜드', '최근', '이번', '내년', '평균', '전국', '가운데', '력사', '정부', '이달', '스타', '당시', '번지', '만들', '앞두', '들어서', '가깝', '보이', '세상', '반면', '이끌', '건설', '건설사', '상황', '활용', '이후', '지난해', '관련', '기간', '해당', '기자', '분기', '연내', '기사', '진행', '이날', '더불', '안내', '요구', '제공', '변호사', '그러', '보도', '나오', '다음', '구체', '그렇', '광고', '시간', '공간', '여부', '관심', '집중', '향후', '제외', '마지막', '작년', '여자', '적용', '아파트', '이상', '경우', '일반', '세대', '인근', '가격', '대비', '예상', '기대', '이용', '마련', '상승', '결과', '시작', '가치', '부문', '주변', '포함', '주요', '비율', '다양', '전체', '지속', '단계', '과정', '분야', '기존', '건설업', '베스트', '보유', '신청', '편리', '지난달', '추가', '미래', '모집', '특별', '상반기', '우수', '활동', '완료', '고급', '최초', '위주', '본격', '영향', '자리', '사업자', '성공', '확인', '일부', '일정', '인기', '전년', '세계', '비교', '경제', '마무리', '안정', '국토', '정도', '국가', '실시', '특화', '고려', '반영', '비용', '상태', '실사', '현재', '처음', '이어지', '이전', '차지', '실제', '몰리', '나서', '하반기', '한편', '대부분', '생각', '이하', '처리', '국민', '본부', '사람', '장동', '가지', '디에이치', '홈페이지', '도래', '사유', '니스', '포트', '엑스', '풀이', '파이', '최선', '사진', '이내', '파워', '광역시', '도움', '계기', '유입', '어려움', '계속', '부장', '뉴스', '나라', '유리', '신재', '공기', '지금', '목소리', '긍정', '상한', '상당', '주력', '합리', '갖추', '원회', '차이', '임시', '그동안', '조기', '선보이', '차환', '대신', '결국', '초과', '절반', '현실', '시대', '꼽히', '요약', '극대', '기여', '늘어나', '내놓', '오르', '불리', '스퀘어', '이름', '대우', '부족', '최소', '전날', '예고', '평면', '빠르', '총액', '과거', '원가', '시점', '연간', '시기', '역대', '관계', '어렵', '부분', '연속', '형성', '여건', '명회', '급등', '커지', '달하', '취소', '전반', '동시', '이르', '역할', '주비', '기본', '상위', '각종', '가량', '주액', '타입', '제기', '최종', '감소', '일대', '적극', '일원', '변경', '수준', '설명', '분류', '섹션', '예정', '중단', '증가', '회사', '최고', '기록', '게임', '오늘', '사이', '오전', '사실', '여성','총괄', '기타', '신영', '작용', '실거', '위축', '새롭', '누적', '사모', '반경', '한울', '이외', '문의', '여파', '눈길', '가족', '단위', '당기', '단기', '당초', '가든', '정기', '선택', '내달', '실시간', '단독', '흐름', '특징', '비엘', '곳곳', '공식', '만기', '양사', '계층', '평형', '장점', '유진', '현황', '중흥', '사업', '토건', '가구', '기준','직주','이어지']

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
df4 = make_tokens(df3)

# 불용어 처리
# 제목은 처리 안함
# 단어 빈도수 오름차순 정리
# 불용어 리스트 작성
#Cwords_list = df4['tokens'].str.split()
#all_Cwords = [word for words in Cwords_list for word in words]
#Cword_counts = Counter(all_Cwords)
#most_common_Cwords = Cword_counts.most_common(500)

#print("제목에서 가장 많이 나온 상위 500개 단어:")
#for word, count in most_common_Cwords:
    #print(f"{word}: {count}")

# print(DF)
df4.to_csv('LH_23.csv', index = False)