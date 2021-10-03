import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NanumBarunpenB.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


corona_all=pd.read_csv('서울시 코로나19 확진자 현황.csv', encoding='euc-kr')
#print(corona_all.head())

#drop 함수를 사용하여 정보가 없는 데이터 삭제
corona_del_col = corona_all.drop(columns = ['국적','환자정보','조치사항'])

#print(corona_del_col['확진일'])

month = []
day = []
for data in corona_del_col['확진일']:
    month.append(data.split('-')[1])
    day.append(data.split('-')[2])

corona_del_col['month'] = month
corona_del_col['day'] = day

corona_del_col['month'].astype('int64')
corona_del_col['day'].astype('int64')
print(corona_del_col['month'])
print(corona_del_col['day'])
order = []
for i in range(1,11):
    order.append(str(i))

# 그래프의 사이즈를 조절.
plt.figure(figsize=(15,5))

# seaborn의 countplot 함수를 사용하여 출력.
sns.set(style="darkgrid")
#sns.countplot(x="month", data=corona_del_col, palette="Set2", order = order)

# series의 plot 함수를 사용한 출력 방법.
corona_del_col['month'].value_counts().plot(kind='bar')
plt.title("월별 서울시 코로나 확진자 수",fontproperties=font)
plt.show()