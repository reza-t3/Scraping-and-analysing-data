import pandas as pd

# df = data_frame
df = pd.read_csv('car_table.csv')


answer1_1 = df[df['company']=='peugeot'].car.unique()
answer1_2 = df[df['company']=='hyundai'].car.unique()
# print(answer1_1)
# print(answer1_2)


answer2 = df[((df['year']<=1400) & (df['year']>=1395)) | ((df['year']<=2022) & (df['year']>=2017))]
#print(answer2['car'].count())


answer3_1 = df[df['car']=='206sd'].tream.unique()
#print(len(answer3_1))
answer3_2_1 = df[df['car']=='206sd'].tream.describe()
answer3_2_2 = df[df['car']=='206sd'].tream.value_counts().idxmax()
#print(answer3_2_2)


series1 = df[df['year']>1401]['kilometer'] / (2023 - df[df['year']>1401]['year'])
series2 = df[df['year']<1401]['kilometer'] / (1401 - df[df['year']<1401]['year'])
#print(series1.max(),series2.max())
#print(series2.nlargest(2))
#print(df.loc[series2.idxmax()])
#print(df.loc[11151]) # second largest


answer5 = df[df['price']>0].groupby(by='company').price.mean().idxmax()
#print(answer5)


answer6 = df['car'].value_counts().idxmax()
#print(answer6)


answer7_1 = df[df['price']>0][df['car']=='206'][(df['year']>=1385) & (df['year']<=1392)].price.mean()
answer7_2 = df[df['price']>0][df['car']=='206'][(df['year']>=1393) & (df['year']<=1400)].price.mean()
#print(int(answer7_2)-int(answer7_1))