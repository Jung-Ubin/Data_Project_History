import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point
import matplotlib.font_manager as fm
import matplotlib as mpl

# 한글 폰트 설정 (예: 맑은 고딕)
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
mpl.rc('font', family=font_name)

# 마이너스 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False

# 1. 동작구 경계 불러오기
gdf = gpd.read_file('C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_시군구_경계/sig.shp', encoding='cp949')
gdf = gdf.set_crs("EPSG:5179").to_crs("EPSG:4326")
dongjak_gdf = gdf[gdf['SIG_CD'] == '11590']

# 2. 버스 정류장 좌표 CSV 불러오기
bus_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_동작구_정류장_좌표추출.csv", encoding='utf-8-sig')
bus_gdf = gpd.GeoDataFrame(
    bus_df,
    geometry=[Point(xy) for xy in zip(bus_df["x_좌표"], bus_df["y_좌표"])],
    crs="EPSG:4326"
)

# 3. 지하철역 좌표 CSV 불러오기
subway_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_동작구_지하철역_좌표데이터.csv", encoding='utf-8-sig')
subway_gdf = gpd.GeoDataFrame(
    subway_df,
    geometry=[Point(xy) for xy in zip(subway_df["경도"], subway_df["위도"])],
    crs="EPSG:4326"
)

# 4. 따릉이 대여소 좌표 CSV 불러오기
# 따릉이 대여소 데이터 읽어오기
bike_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/04_동작구_따릉이대여소_좌표데이터.csv", encoding='cp949')

# 따릉이 대여소 GeoDataFrame으로 변환
bike_gdf = gpd.GeoDataFrame(
    bike_df,
    geometry=[Point(xy) for xy in zip(bike_df["경도"], bike_df["위도"])],
    crs="EPSG:4326"
)

# 5. 시각화
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# 배경 경계
dongjak_gdf.plot(ax=ax, edgecolor='black', facecolor='white')


# 버스 정류장
bus_gdf.plot(ax=ax, color='red', 
             markersize=10, 
             label='버스정류장'
)

# 지하철역
subway_gdf.plot(
    ax=ax,
    facecolor='blue',
    edgecolor='black',
    markersize=40,
    linewidth=0.5,
    label='지하철역'
)

# 따릉이 대여소
bike_gdf.plot(
    ax=ax,
    facecolor='green',
    edgecolor='black',
    markersize=30,
    linewidth=0.5,
    label='따릉이대여소'
)

# 제목 및 스타일
plt.title("동작구 버스 정류장, 지하철역, 따릉이 대여소 위치", fontsize=14)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()