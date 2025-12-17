<<<<<<< HEAD
# Day - 4 협업 일지

일자: 2025-05-20 / 정유빈

---

### 팀원들과 앞으로 할 일 의논

- 동작구 작업 / 성동구 작업 3 팀으로 나눠서 작업 진행해보기.
- 동 별 총 생활인구 수 파악하고 각 동별 시각화 작업 진행해보기.

# \* 내가 한 일

- 동작구 내 동 경계 나눠서 색 채울 수 있는지 확인
- 테블루를 사용하여 csv 파일과 shp공간 파일을 겹쳐서 사용하는 작업 진행

- 동작구 대중교통 위치 좌표, 인구 밀집도 둘 다 적용된 시각화 자료와  
  동작구 대중교통 좌표 지도 , 동작구 인구밀집도 지도 3개를 만들어보고,  
  어느것이 시각화 했을 때 보기 편한지 확인

- 팀원들과 대중교통에서의 어떤 문제점이 있는지 얘기해보고  
  보완점, 개선점이 뭐가 있을지 의논함

- 동작구 데이터 지하철, 버스, 따릉이 위치 ,동 / GID 컬럼 생성해서  
  다시 전처리 진행

- 동작구 격자(100m)별 생활인원 shp 파일을 쪼개서  
  각 구역의 위도 경도 값을 구하여 오차범위 조건을 걸고  
  그 오차범위 내 지역의 정류장, 역, 따릉이대여소 수를 세는 코드 작성

  일단 shp 파일 쪼개서 위도 경도값 부터 csv파일로 구하는 작업부터 진행

- shp 좌표 값을 정류장, 역 위치와 비교하여  
  격자 구간 중심 좌표 기준 가장 인접한 지하철역 거리 & 150, 300, 450m 반경 내 있는 정류장 개수  
  계산해서 csv 파일로 제작

---

# \* 오늘 코딩

(동작구*격자 단위*중심좌표 반경*인접정류장*개수)

```python
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Haversine 거리 계산 함수 (단위: 미터)
def haversine(lon1, lat1, lon2, lat2):
    R = 6371000  # 지구 반지름 (m)
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2)**2 + cos(phi1) * cos(phi2) * sin(dlambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 생활인구 격자 중심 좌표 불러오기
D_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/07_동작구_생산가능인구수격자(100m)/08_동작구_생활인구_격자_좌표.csv", encoding="utf-8-sig")

# 버스 정류장 데이터 불러오기
bus_station_data = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_공공_서울시 버스정류소 위치정보.csv", encoding="cp949")
bus_station_data = bus_station_data[["정류소명", "X좌표", "Y좌표"]]

# 반경 거리 기준 설정
radius_list = [150, 300, 400]

# 각 반경에 대해 정류장 개수 저장할 컬럼 초기화
for r in radius_list:
    D_df[f"반경{r}m_정류장수"] = 0

# 거리 계산 및 반경 내 정류장 수 카운트
for i, grid in D_df.iterrows():
    grid_lon = grid["경도"]
    grid_lat = grid["위도"]
    counts = {r: 0 for r in radius_list}

    for _, station in bus_station_data.iterrows():
        station_lon = station["X좌표"]
        station_lat = station["Y좌표"]

        dist = haversine(grid_lon, grid_lat, station_lon, station_lat)

        for r in radius_list:
            if dist <= r:
                counts[r] += 1

    for r in radius_list:
        D_df.at[i, f"반경{r}m_정류장수"] = counts[r]

# 결과 저장
D_df.to_csv("동작구_격자_정류장반경_결과.csv", index=False, encoding="utf-8-sig")

```

---

# 노트 (생각나는것 아무거나 작성하면서 고민)

- 오늘 너무 바뻐서 다른 적을 것이 없음.

---

# \* 문제점

- 팀원들과의 데이터 수집 작업 중 중복으로 일이 겹치는 일이 생김  
  소통 후 정리하여 수집 작업 재정립

- 코드 작성 시 반복문 사용을 불필요하게 사용해서(오늘 코드) 작업이 오래걸림  
  if 조건을 달아서 효율성을 늘리자(ex: 최대 반경 400m에 포함되는 데이터만 분석하는 조건)

# \* 회고

- 팀원들과 많은 소통을 하였지만, 수집 과정에서 겹치는 구간이 발생했다.  
  팀원들이 어떤 데이터를 수집하고 있는지 인지하고 효율적으로 수집, 분석하자

- 코드 작성 시 for문 사용할 때 데이터가 크다면 조건을 걸어서 효율적으로 사용하자
=======
# Day - 4 협업 일지

일자: 2025-05-20 / 정유빈

---

### 팀원들과 앞으로 할 일 의논

- 동작구 작업 / 성동구 작업 3 팀으로 나눠서 작업 진행해보기.
- 동 별 총 생활인구 수 파악하고 각 동별 시각화 작업 진행해보기.

# \* 내가 한 일

- 동작구 내 동 경계 나눠서 색 채울 수 있는지 확인
- 테블루를 사용하여 csv 파일과 shp공간 파일을 겹쳐서 사용하는 작업 진행

- 동작구 대중교통 위치 좌표, 인구 밀집도 둘 다 적용된 시각화 자료와  
  동작구 대중교통 좌표 지도 , 동작구 인구밀집도 지도 3개를 만들어보고,  
  어느것이 시각화 했을 때 보기 편한지 확인

- 팀원들과 대중교통에서의 어떤 문제점이 있는지 얘기해보고  
  보완점, 개선점이 뭐가 있을지 의논함

- 동작구 데이터 지하철, 버스, 따릉이 위치 ,동 / GID 컬럼 생성해서  
  다시 전처리 진행

- 동작구 격자(100m)별 생활인원 shp 파일을 쪼개서  
  각 구역의 위도 경도 값을 구하여 오차범위 조건을 걸고  
  그 오차범위 내 지역의 정류장, 역, 따릉이대여소 수를 세는 코드 작성

  일단 shp 파일 쪼개서 위도 경도값 부터 csv파일로 구하는 작업부터 진행

- shp 좌표 값을 정류장, 역 위치와 비교하여  
  격자 구간 중심 좌표 기준 가장 인접한 지하철역 거리 & 150, 300, 450m 반경 내 있는 정류장 개수  
  계산해서 csv 파일로 제작

---

# \* 오늘 코딩

(동작구*격자 단위*중심좌표 반경*인접정류장*개수)

```python
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Haversine 거리 계산 함수 (단위: 미터)
def haversine(lon1, lat1, lon2, lat2):
    R = 6371000  # 지구 반지름 (m)
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2)**2 + cos(phi1) * cos(phi2) * sin(dlambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 생활인구 격자 중심 좌표 불러오기
D_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/07_동작구_생산가능인구수격자(100m)/08_동작구_생활인구_격자_좌표.csv", encoding="utf-8-sig")

# 버스 정류장 데이터 불러오기
bus_station_data = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/02_공공_서울시 버스정류소 위치정보.csv", encoding="cp949")
bus_station_data = bus_station_data[["정류소명", "X좌표", "Y좌표"]]

# 반경 거리 기준 설정
radius_list = [150, 300, 400]

# 각 반경에 대해 정류장 개수 저장할 컬럼 초기화
for r in radius_list:
    D_df[f"반경{r}m_정류장수"] = 0

# 거리 계산 및 반경 내 정류장 수 카운트
for i, grid in D_df.iterrows():
    grid_lon = grid["경도"]
    grid_lat = grid["위도"]
    counts = {r: 0 for r in radius_list}

    for _, station in bus_station_data.iterrows():
        station_lon = station["X좌표"]
        station_lat = station["Y좌표"]

        dist = haversine(grid_lon, grid_lat, station_lon, station_lat)

        for r in radius_list:
            if dist <= r:
                counts[r] += 1

    for r in radius_list:
        D_df.at[i, f"반경{r}m_정류장수"] = counts[r]

# 결과 저장
D_df.to_csv("동작구_격자_정류장반경_결과.csv", index=False, encoding="utf-8-sig")

```

---

# 노트 (생각나는것 아무거나 작성하면서 고민)

- 오늘 너무 바뻐서 다른 적을 것이 없음.

---

# \* 문제점

- 팀원들과의 데이터 수집 작업 중 중복으로 일이 겹치는 일이 생김  
  소통 후 정리하여 수집 작업 재정립

- 코드 작성 시 반복문 사용을 불필요하게 사용해서(오늘 코드) 작업이 오래걸림  
  if 조건을 달아서 효율성을 늘리자(ex: 최대 반경 400m에 포함되는 데이터만 분석하는 조건)

# \* 회고

- 팀원들과 많은 소통을 하였지만, 수집 과정에서 겹치는 구간이 발생했다.  
  팀원들이 어떤 데이터를 수집하고 있는지 인지하고 효율적으로 수집, 분석하자

- 코드 작성 시 for문 사용할 때 데이터가 크다면 조건을 걸어서 효율적으로 사용하자  
>>>>>>> d13e419506e0b12e6cb413498af7ff92d00164cd
