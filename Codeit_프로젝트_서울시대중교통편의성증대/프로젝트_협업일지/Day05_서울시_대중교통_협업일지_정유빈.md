# Day - 5 협업 일지

일자: 2025-05-21 / 정유빈

---

### 팀원들과 앞으로 할 일 의논

- 내일 멘토링 수업 전까지 어느정도 결과물이 나와야 됨
- 시각화 정리를 다시 해보기

- 특정 정류장들이 어느 격자에 포함되는지 확인

- 동작구, 성동구 지역을 격자100m단위로 나눈 칸 중심좌표 기준  
  정류장들의 좌표와 확인해보기

- 동작구 성동구 지역의 버스정류장의 좌표마다,  
  도로명 주소 얻는 코드 확인해보기

- 성동구도 마찬가지로 진행해보기

# \* 내가 한 일

- 동작구, 성동구 지역을 격자100m단위로 나눈 칸 중심좌표 기준  
  정류장들의 좌표와 정류장 NODE_ID를 csv 파일 제작하기

- 위 csv 파일을 어제 만든 중심좌표기준 가까운 지하철역 데이터와 합쳐보기.

- 첫 번째에서 만든 데이터 내에 있는 좌표를 사용하여 주소 알아내는 코드 알아보기

- 동작구/성동구 내 버스 정류장 좌표 데이터를 카카오 api를 사용하여 주소로 변환

- 변환한 주소 데이터가 지번이어서 도로명으로 변환 작업 필요 > 팀원들이 도로명이 필요하다고 했음

- 주소를 도로명으로 변환할 수 있는 사이트에 자동으로 csv파일 내 행 별로 주소를 입력하여  
  새로운 도로명 컬럼에 도로명 주소를 추가, 도로명 주소가 없는 지역이면 '-' 로 추가하는 코드 작성

---

# \* 오늘 코딩

(동작구 격자 내 정류장 좌표 및 정류장 NODE_ID 추출 후 csv 파일 생성)

```python
import pandas as pd
from geopy.distance import geodesic
# geopy: 지리 정보를 다루는 파이썬 라이브러리 (위도/경도 기반).
# geodesic: 지구 곡률을 고려한 두 지점 간의 거리(최단 거리, 즉 "대권거리")를 계산.

dongjak_grid_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/07_동작구_생산가능인구수격자(100m)/07_동작구_생활인구_격자_좌표.csv", encoding="utf-8-sig")

dongjak_bus_df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/05_동작구_지하철&버스&따릉이&버스노선수_좌표.csv", encoding="utf-8-sig")


# 버스 정류장 데이터 필터링
bus_df = dongjak_bus_df[dongjak_bus_df["버스 여부(Y/N)"] == "Y"].copy()
bus_df = bus_df[["역(정류장)", "x_좌표", "y_좌표", "동_이름", "NODE_ID"]]  # NODE_ID 포함

# 격자 데이터 정리
grid_df = dongjak_grid_df[["GID", "위도", "경도", "생활인구수"]].copy()

results = []

for _, row in grid_df.iterrows():
    gid = row["GID"]
    grid_lat = row["위도"]
    grid_lon = row["경도"]
    population = row["생활인구수"]

    for _, stop in bus_df.iterrows():
        stop_lat = stop["y_좌표"]
        stop_lon = stop["x_좌표"]
        distance = geodesic((grid_lat, grid_lon), (stop_lat, stop_lon)).meters

        if distance <= 50:  # 반경 50m
            results.append({
                "GID": gid,
                "gid위도": grid_lat,
                "gid경도": grid_lon,
                "생활인구수": population,
                "동 이름": stop["동_이름"],
                "gid 버스정류장명": stop["역(정류장)"],
                "gid버스정류장위도": stop_lat,
                "gid버스정류장경도": stop_lon,
                "NODE_ID": stop["NODE_ID"]
            })

# 결과 DataFrame 생성
result_df = pd.DataFrame(results)

# CSV로 저장
result_df.to_csv("동작_격자별_정류장_좌표매치.csv", index=False, encoding="utf-8-sig")
```

---

# 노트 (생각나는것 아무거나 작성하면서 고민)

- 보고서 작성 할 때 제목 > 목차(차례) > 분석 계기 > 분석 결과 및 결론 > 분석을 뒷받침하는 시각화 자료  
  \> 분석을 뒷받침하는 통계적 데이터 > 데이터 출처 및 마무리  
  이런 과정으로 생각을 해봐야 겠다.

---

# \*문제점

- 아직 코딩 시 모르는 라이브러리와 코드들이 많고, 데이터 전처리 시 컬럼 기준을 세울 때 햇갈림.  
  파일을 결국 하나로 합치는것은 포기, 파일 4개로 분리하여 해결함.  
  (동작구/성동구*격자*중심좌표*반경별*정류장*수, 동작구/성동구*격자*중심좌표*기준*가까운지하철역*거리)

- 보고서의 기본적인 틀이 아직 안잡힘.  
  팀원들과 이야기를 했고, 데이터를 준비했지만 보고서 작성은 준비안됨.  
  슬슬 준비를 해야함(아직 해결이 안됨)

# \* 회고

- 보고서 작성을 어떤식으로 해야할지 조금 더 생각을 해봐야겠다.  
  단순하게 끝내기에는 너무 어려운 주제여서 조금 더 좋은 아이디어가 있으면 좋을 것 같다.

- 데이터 찾는 요령을 확실히 많이 키워야 될 것 같다.
