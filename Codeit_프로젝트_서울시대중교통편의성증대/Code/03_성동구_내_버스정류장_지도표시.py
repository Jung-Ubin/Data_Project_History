import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point
import matplotlib.font_manager as fm
import matplotlib as mpl


# 한글 폰트 설정 (예: 맑은 고딕)
font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우 기본 한글 폰트
font_name = fm.FontProperties(fname=font_path).get_name()
mpl.rc('font', family=font_name)

# 마이너스 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False

# 1. 성동구 경계 불러오기
gdf = gpd.read_file('C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_시군구_경계/sig.shp', encoding='cp949')
gdf = gdf.set_crs("EPSG:5179").to_crs("EPSG:4326")
Sungdong_gdf = gdf[gdf['SIG_CD'] == '11200']

# 2. 저장된 정류장 좌표 CSV 불러오기
s_bus_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/03_성동구_정류장_좌표추출.csv", encoding='utf-8-sig')

# 3. GeoDataFrame으로 변환
s_bus_gdf = gpd.GeoDataFrame(
    s_bus_df,
    geometry=[Point(xy) for xy in zip(s_bus_df["x_좌표"], s_bus_df["y_좌표"])],
    crs="EPSG:4326"
)

# 4. 시각화
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# 성동구 경계 그림
Sungdong_gdf.plot(ax=ax, edgecolor='black', facecolor='white')

# 버스정류장 핀 (빨간 점)
s_bus_gdf.plot(ax=ax, color='red', markersize=10)

# 제목 및 스타일
plt.title("성동구 버스 정류장 위치", fontsize=14)
plt.tight_layout()
plt.show()
