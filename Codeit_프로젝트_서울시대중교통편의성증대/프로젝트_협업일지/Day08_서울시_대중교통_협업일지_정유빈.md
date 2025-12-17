# Day - 8 협업 일지

일자: 2025-05-26 / 정유빈

---

### 팀원들과 한 작업

- 보고서 위주로 작업 진행

# \* 내가 한 일

- 보고서 분석 배경 및 내용들 팀원들과 같이 회의

- 1. 분석 배경이 내용이 너무 많은 것 같다. 좀 덜어서 작성해보자  
     => 서울시 교통 관련 생활과 가장 밀접한 부분은 대중교통이다,  
      서울시도 시민들의 편리한 대중교통 이용을 위해 노력하고있다  
      서울시의 데이털르 활용하여 ... 이런식으로 작성해보자.

- 2. 사진으로 설명하는것이 좋을지? 글로 설명하는것이 좋을지?  
     => 둘 다 만들어서 확인해서 더 좋은 것을 사용하기

- 3. 사용한 코드 정리하여 제출 파일에 작성

- 보고서에 사용할 데이터 테블루로 시각화하기  
  행정동별 정류장, 노선 분석하여 [시각화 (클릭하여 그래프 확인 가능)](https://public.tableau.com/app/profile/.75452252/viz/_17482438067160/1_1?publish=yes).

---

# \* 오늘 코딩

(동작구 내 버스정류장 지번주소 > 도로명 주소로 바꾸기(웹크롤링 사용))

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# ChromeDriver 자동 설치 및 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(3)

# 결과 저장 리스트
도로명_주소 = []

# CSV 파일 읽기
df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/10_동작_성동_버스정류장_도로명주소/10_동작_버스정류장위치_데이터(지번주소).csv", encoding="utf-8-sig")
dongjak_busstation_df = pd.DataFrame(df)
col = dongjak_busstation_df['주소']

# 기본 검색 URL
base_url = "https://www.juso.go.kr/support/AddressMainSearch.do?searchKeyword="

# 주소 수만큼 반복
for i in range(len(col)):
    address = str(col[i])
    driver.get(base_url + address)
    time.sleep(2)

    try:
        road_name = driver.find_element(By.XPATH, '//*[@id="list1"]/div[1]/span[2]').text
    except:
        road_name = '도로명불명'

    도로명_주소.append(road_name)

# 동작구 도로명 주소 결과 저장
dongjak_busstation_df['도로명'] = 도로명_주소
dongjak_busstation_df.to_csv('동작_버스정류장주소_도로명.csv', index=False, encoding="utf-8-sig")

driver.quit()
```

---

# 노트 (생각나는것 아무거나 작성하면서 고민)

- 저번주에 나왔던 해결책(재개발 되는 지역이 있으니 버스 노선 개선해야함 등)을 사용하여  
  보고서를 작성하기.

---

# \*문제점

- 복잡해보이고 설명이 길어져서 보고서가 가독성이 떨어졌음.  
  필요한 내용만 적고, 뒷 내용으로 갈 때 설명을 적자는 의견으로 앞 내용 압축하여 해결

- 내용은 어느정도 나왔는데 어떻게 정리할지 아직 고민이 많음  
  적당한 다른 보고서 예시들을 보고 활용해보자는 의견이 나옴.

- 머신러닝 데이터에서 문제가 발견됐음  
  지역 필터링을 하는데 있어서 수정 사항이 제대로 반영되지 않음
  필터링 조건을 줄이는 과정에서 실수로 들어가야되는 조건이 빠지고 다른 조건이 들어가 결과값이 다르게 출력됨
  다시 수정하여 문제 해결

# \* 회고

- 보고서 작성할 때 어디서부터 시작하고 어떻게 정리할지 바로 생각이 나지 않음  
  아직 요령도 부족하고 사용한 데이터들이 많은데 정리가 잘 안됨.  
  필요한 내용만 딱 뽑아서 정리할 수 있는 능력을 키워야겠다는 생각이 듦.
