import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 지도 출력을 위한 라이브러리 folium을 import 합니다.
import folium

# Map 함수를 사용하여 지도를 출력합니다.
map_osm = folium.Map(location=[37.529622, 126.984307], zoom_start=11)
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

corona_del_col['month'].astype('unicode')
corona_del_col['day'].astype('unicode')
#print(corona_del_col['month'])
#print(corona_del_col['day'])
order = []
for i in range(1,13):
    if i<10:
        order.append('0'+str(i))
    else:
        order.append(str(i))


# 월별 서울시 코로나 확진자 수
# 그래프의 사이즈를 조절.
plt.figure(figsize=(15,5))

# seaborn의 countplot 함수를 사용하여 출력.
sns.set(style="darkgrid")
sns.countplot(x="month", data=corona_del_col, palette="Set2", order = order)

# series의 plot 함수를 사용한 출력 방법.
#corona_del_col['month'].value_counts().plot(kind='bar')
#plt.title("월별 서울시 코로나 확진자 수",fontproperties=font)


#2020년 8월달 일별 확진자 수 출력
order2 =[]
for i in range(1,32):
    if i<10:
        order2.append('0'+str(i))
    else:
        order2.append(str(i))
#print(order2)
plt.figure(figsize=(15,10))
sns.set(style="darkgrid")
ax = sns.countplot(x="day", data=corona_del_col[corona_del_col['month']=='08'], palette="rocket_r", order=order2)


#지역별 확진자 수 
plt.figure(figsize=(15,20))
sns.set(font=font,style='darkgrid')
ax = sns.countplot(x="지역", data=corona_del_col, palette="Set2")
#plt.show()
corona_out_region = corona_del_col.replace({'종랑구':'중랑구', '한국':'기타'})

#서울 지역에서 확진자를 지도에 출력
map_osm = folium.Map(location=[37.529622, 126.984307], zoom_start=11)
CRS=pd.read_csv("서울시 행정구역 시군구 정보 (좌표계_ WGS1984).csv")
corona_seoul = corona_out_region.drop(corona_out_region[corona_out_region['지역'] == '타시도'].index)
corona_seoul = corona_seoul.drop(corona_out_region[corona_out_region['지역'] == '기타'].index)

# 서울 중심지 중구를 가운데 좌표로 잡아 지도를 출력합니다.
map_osm = folium.Map(location=[37.557945, 126.99419], zoom_start=11)

# 지역 정보를 set 함수를 사용하여 25개 고유의 지역을 뽑아냅니다.
for region in set(corona_seoul['지역']):

    # 해당 지역의 데이터 개수를 count에 저장합니다.
    count = len(corona_seoul[corona_seoul['지역'] == region])
    # 해당 지역의 데이터를 CRS에서 뽑아냅니다.
    CRS_region = CRS[CRS['시군구명_한글'] == region]

    # CircleMarker를 사용하여 지역마다 원형마커를 생성합니다.
    marker = folium.CircleMarker([CRS_region['위도'], CRS_region['경도']], # 위치
                                  radius=count/10 + 10,                 # 범위
                                  color='#3186cc',            # 선 색상
                                  fill_color='#3186cc',       # 면 색상
                                  popup=' '.join((region, str(count), '명'))) # 팝업 설정
    
    # 생성한 원형마커를 지도에 추가합니다.
    marker.add_to(map_osm)

map_osm.save('map.html')