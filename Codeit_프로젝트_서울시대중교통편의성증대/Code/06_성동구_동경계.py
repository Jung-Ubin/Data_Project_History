import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.font_manager as fm
import matplotlib as mpl

# 한글 폰트 설정 (예: 맑은 고딕)
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
mpl.rc('font', family=font_name)

# 마이너스 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False


# 읍면동 Shapefile 불러오기
emd_path = 'C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/06_읍면동_경계/emd.shp'
gdf_emd = gpd.read_file(emd_path, encoding='cp949')

# 좌표계 변환 (EPSG:5179 → WGS84)
gdf_emd = gdf_emd.set_crs("EPSG:5179").to_crs("EPSG:4326")

# 성동구 필터링 (EMD_CD 앞 5자리: 11200 → 성동구)
gdf_seongdong = gdf_emd[gdf_emd['EMD_CD'].str.startswith('11200')]

# 시각화
plt.figure(figsize=(8, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# 성동구 동 경계
gdf_seongdong.plot(ax=ax, color='white', edgecolor='black', linewidth=1)

# 타이틀 및 스타일
plt.title("서울시 성동구 행정동 경계도(법정동기준)", fontsize=14)
plt.tight_layout()
plt.show()
