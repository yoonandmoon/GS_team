import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_data(url):
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    return pd.read_html(html.text, header=0)[0]

base_url = 'https://finance.naver.com/item/sise_day.nhn?code=006360&page='
df = pd.DataFrame()

for page in range(1, 16):
    url = f'{base_url}{page}'
    data = get_data(url)
    df = df.append(data, ignore_index=True)

# 데이터 필터링
df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d')
df = df[(df['날짜'] >= '2023-04-02') & (df['날짜'] <= '2023-09-02')]

# 필요한 열만 선택
df = df[['날짜', '종가', '거래량']]

# 날짜 기준으로 내림차순 정렬
df = df.sort_values(by='날짜', ascending=True)

# CSV 파일로 저장 (날짜 역순으로 저장)
df.to_csv('gs_stock.csv', index=False)