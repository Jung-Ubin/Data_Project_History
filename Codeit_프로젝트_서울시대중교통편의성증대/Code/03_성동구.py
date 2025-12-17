import cartopy.crs as ccrs
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

fname = 'C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_시군구_경계/sig.shp'
gdf = gpd.read_file(fname, encoding='cp949')
gdf.geometry = gdf.geometry.set_crs("EPSG:5179")
gdf.geometry = gdf.geometry.to_crs("EPSG:4326")

"""
gdf 파일에는 SIG_CD: 지역 코드 정보가 있음음
지역 코드의 앞부분 숫자 두개는 도시의 지역 코드
서울의 지역 코드는 11이므로 SIG_CD의 앞에 두 자리가 11인 행을 선택(11290)
"""
gdf_seoul = gdf[gdf['SIG_CD'].str.startswith('11200')] # 성동구

plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
gdf_seoul.plot(ax=ax, lw=1, color='white', edgecolor='black')
plt.show()