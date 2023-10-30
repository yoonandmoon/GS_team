import pandas as pd
import os

directory = 'C:\\DA\\GSTEAM\\GS_team\\01pretreatment\\csv\\news\\pretreat_news'  # CSV 파일들이 있는 디렉토리의 경로로 변경하세요.

# 해당 디렉토리 내의 모든 CSV 파일을 리스트업
all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]

# 각 파일을 데이터프레임으로 읽어 리스트에 저장
dfs = [pd.read_csv(file) for file in all_files]

# 모든 데이터프레임을 하나로 합치기
combined_df = pd.concat(dfs, ignore_index=True)

# 결과를 새 CSV 파일로 저장
combined_df.to_csv('news_combined.csv', index=False)