import pandas as pd

dfA = pd.read_csv('C:/Users/rhksa/OneDrive/바탕 화면/gs project/GS_team/01pretreatment/csv/stock/R_gs_stock(ver.210801_231027).csv')
dfB = pd.read_csv('C:\\Users\\rhksa\\OneDrive\\바탕 화면\\gs project\\GS_team\\01pretreatment\\csv\\news\\pretreat_news\\GS_news2108_2310(ver.C01).csv')

result = dfA.merge(dfB, on='date', how='inner')

result.to_csv('stock_news_combine.csv',index=False)





