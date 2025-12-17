# Day - 7 협업 일지

일자: 2025-05-23 / 정유빈

---

### 팀원들과 앞으로 할 일 의논

- 어제 멘토님께 피드백 받았던 내용 정리하여 적용할지 생각하기

- 동작구/성동구 노선 데이터 찾아보기

- 우리가 배운 분석 방법 중 어떤걸 사용할지 생각하기

# \* 내가 한 일

- 카카오 API를 이용해서 서울시 버스노선 정보 찾아보기

- 공공데이터에서 제공하는 API로 버스 노선 경로정보 수집

- 지도 보면서 대중교통 취약지역이라 생각되는 지역 찾기

---

# \* 오늘 코딩

(서울시 버스 노선 경로 관련 정보 요청)

```python
import requests
import pandas as pd
import xmltodict


# ▶ 인증키 입력
SERVICE_KEY = "----"

# ▶ API 호출 URL
url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getRoutePath"

# ▶ 전체 노선 목록 요청 (busRouteNm 빈 문자열로 전체 조회)
params = {
    "serviceKey": SERVICE_KEY,
    "busRouteNm": ""
}

res = requests.get(url, params=params)
data = xmltodict.parse(res.text)

try:
    item_list = data["ServiceResult"]["msgBody"]["itemList"]

    # item_list가 dict (1건)일 수 있으므로 리스트화
    if isinstance(item_list, dict):
        item_list = [item_list]

    # pandas DataFrame으로 변환 후 저장
    df = pd.DataFrame(item_list)
    df.to_csv("전체_버스노선_API_조회결과.csv", index=False, encoding="utf-8-sig")
    print("저장 완료: 전체_버스노선_API_조회결과.csv")

except Exception as e:
    print("데이터 파싱 실패:", e)

```

---

# 노트 (생각나는것 아무거나 작성하면서 고민)

- 카카오 API를 사용해서 동작구 성동구 버스 노선 데이터 뽑을 수 있는지 알아보자.  
  카카오 API, 네이버 API 실패

- 버스 노선경로 데이터 api를 끌고오려했는데 사이트 오류로 실패  
  오류 신고 후 다음주에 신고 피드백 확인

---

# \*문제점

- 동작구 지도를 보면서 버스 노선과, 정류장, 역 위치 등 취약지역 분석을 했지만 찾기 쉽지가 않다.  
  꾸준히 탐색을 해서 무엇인지 문제점을 찾아봐야한다.

- 통계적 분석이 부족할 것 같은데 지금 까지 문제점과 개선점 찾기에 팀원들이 집중해있다.  
  다음주에 한번 통계적 분석이 부족하지 않은지 이야기 해봐야 될 것 같다.

# \* 회고

- 지금까지 데이터 수집을 하면서  
  '이런 데이터가 있을까?' >> "없으면 만들어보자!" >> "데이터를 만들기 위해 어떤 데이터들을 사용할까?"  
  등 계획할 수도 있었고, 생각을 하면서 작업을 했었는데,

  데이터 수집이 거의 끝나고 문제점들을 찾는 과정으로 들어오니  
  위에서 순서나열하듯 세웠던 계획들이 안세워지고, 지도를 오랫동안 계속 쳐다보고,  
  '여기가 문제인건가?', '빌라촌엔 버스가 못다니고 애초에 없을거같은데?", "따릉이 설치할 곳도 마땅치  
   않고.." 등등 계획이 세워지지 않고 답답하고 머리만 어지러웠다.  
  작성하고 있는 지금까지도 모든 팀원들이 지도를 보며 찾고있지만, 찾기 너무 힘들다..

  분명 방법이 있을것 같은데 창의적인 생각이 잘 들지 않는다.

  이 작업을 어떻게 해결해야할지 팀원들과 같이 탐색하고 의견공유를 해야겠다.
