import warnings
warnings.filterwarnings(action='ignore')

import pandas as pd
df = pd.read_csv('C:\\DA\\GSTEAM\\GS_team\\01pretreatment\stock_news_combine.csv')
df2 = df[['date','거래량','Tokens_2']]

result_df = df2.drop_duplicates('date').set_index('date')
result_df['news_stock'] = df2.groupby('date').size()

# 인덱스를 다시 초기화하여 'date' 열을 컬럼으로 되돌립니다.
result_df.reset_index(inplace=True)

df3 = result_df[['date','거래량','news_stock']]

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

X = df3[['거래량']]
y = df3['news_stock']

X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=75)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

y_train = y_train.values.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)
y_train_scaled = scaler.fit_transform(y_train)
y_test_scaled = scaler.transform(y_test)

alpha = 0.01  # L1 규제 강도를 조절할 파라미터
lasso_model = Lasso(alpha=alpha)
lasso_model.fit(X_train_scaled, y_train_scaled)

# 테스트 데이터로 예측
y_pred = lasso_model.predict(X_test_scaled)

# 모델의 성능 평가 (예를 들어, 평균 제곱 오차)
mse = mean_squared_error(y_test_scaled, y_pred)
print(f"Mean Squared Error: {mse}")

# 모델 평가
r2 = r2_score(y_test_scaled, y_pred)
print(f"R-squared: {r2}")