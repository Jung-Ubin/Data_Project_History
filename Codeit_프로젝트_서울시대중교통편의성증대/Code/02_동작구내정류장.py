import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# 1. 동작구 shapefile 불러오기 및 좌표계 맞추기
fname = 'C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_시군구_경계/sig.shp'
gdf = gpd.read_file(fname, encoding='cp949')
gdf.geometry = gdf.geometry.set_crs("EPSG:5179")
gdf = gdf.to_crs("EPSG:4326")

# 2. 동작구만 필터링
dongjak_gdf = gdf[gdf['SIG_CD'] == '11590']  # 또는 'SIG_KOR_NM' == '동작구'

# 3. 정류장 데이터 불러오기
bus_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_공공_서울시 버스정류소 위치정보.csv", encoding='cp949')  # 원본 CSV

# 4. 정류장 좌표를 GeoDataFrame으로 만들기
geometry = [Point(xy) for xy in zip(bus_df['X좌표'], bus_df['Y좌표'])]
bus_gdf = gpd.GeoDataFrame(bus_df, geometry=geometry, crs="EPSG:4326")

# 5. 동작구 내 정류장만 필터링
bus_in_dongjak = bus_gdf[bus_gdf.within(dongjak_gdf.geometry.unary_union)]

# 6. 필요한 컬럼만 선택 + 좌표 분리
result_df = pd.DataFrame({
    "정류장_이름": bus_in_dongjak["정류소명"],  # bus_df에 있는 컬럼럼
    "x_좌표": bus_in_dongjak.geometry.x,
    "y_좌표": bus_in_dongjak.geometry.y
})

# 7. CSV로 저장
result_df.to_csv("동작구_정류장_좌표추출.csv", index=False, encoding='utf-8-sig')
