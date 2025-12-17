# Day - 11 협업 일지(고급)

#### 일자: 25-10-27 / 정유빈

---

### 팀원들과 논의한 일

- 각자 정한 분석 방향으로 분석 진행하면서 공유할 내용 있으면 공유하기

<br>

## \* 오늘 + 내가 한 일

### `device_user_id_summary` 개선 후 재 공유

#### 목적 : `evnet_flow`를 한 번에 붙여서 제작할 때 오류가 발생되어서,

- `hackle_properties` 테이블만 사용
- 원본에서 문자난수/공란/NULL user_id 제거 → `user` ↔ `device` 1:1 → (`user`,`device`,`session`) 완전 중복 제거
- 최종적으로 `device_user_id_summary` `(PK num / device_id / user_id / osname / session_id 집합 / session_count)` 생성

<br>

#### STEP 1 : 문자난수 및 공란 제거 1차 정제

| 항목                              |        결과 |
| --------------------------------- | ----------: |
| 전체 행 수                        |     525,350 |
| 제거된 행 수 (문자난수·공란·NULL) |     191,259 |
| 남은 행 수                        | **334,091** |
| 고유 device_id 수                 |     233,892 |
| 고유 user_id 수 (숫자형만)        | **230,853** |

<br>

→ 문자난수 제거 후 데이터 품질 확보 (약 36% 감소)

---

#### STEP 2 : 여러 device를 사용한 user 제거

| 항목                     |          결과 |
| ------------------------ | ------------: |
| 전체 user 수             |       230,853 |
| 여러 기기 사용 user 수   | 2,555 (1.11%) |
| 한 유저당 평균 device 수 |       1.013대 |
| 한 대만 사용             |     228,298명 |
| 두 대 사용               |       2,300명 |
| 세 대 이상 사용          |         255명 |
| 제거된 행 수             | 7,296 (2.18%) |
| step2 남은 행 수         |   **326,795** |
| 고유 device_id           |       228,251 |
| 고유 user_id             |   **228,298** |

<br>

→ 다중 디바이스를 거친 user 제거로 user ↔ device 1:1 구조 근접

---

#### STEP 3 : 여러 user가 공유한 device 제거

| 항목                         |                  결과 |
| ---------------------------- | --------------------: |
| 여러 user가 연결된 device_id |                  46개 |
| 해당 device 비율             |                 0.02% |
| 관련 행 수                   |         125행 (0.04%) |
| 정제 후 전체 행 수           |           **326,670** |
| 고유 device_id / user_id     | **228,205 / 228,205** |

<br>

→ user ↔ device 완전 1:1 매핑 달성

---

#### STEP 4 : 완전 중복 제거 (user, device, session)

| 항목                   |          결과 |
| ---------------------- | ------------: |
| 전체 행 수             |       228,391 |
| 고유 device_id         |       228,205 |
| 고유 user_id           |       228,205 |
| 고유 session_id        |       228,390 |
| 여러 세션 보유 user 수 | 186명 (0.08%) |

<br>

→ 세션 단위 중복 제거 완료
→ 거의 완전한 1 user : 1 device : 1 session 구조

---

#### STEP 5 : `device_user_id_summary` 최종 생성

| 항목              |               결과 |
| ----------------- | -----------------: |
| 전체 행 수        |        **228,205** |
| 고유 device_id    |        **228,205** |
| 고유 user_id      |        **228,205** |
| session_count ≥ 2 | 약 0.8% (≈1,800행) |

<br>

→ 완벽한 1:1 매핑 기반 테이블 완성
→ 각 행 = “한 디바이스·한 유저”의 모든 세션 통합 정보
→ 한 유저가 앱을 사용한 `device 정보`, `session 정보`가 한 행에 정렬됨

---

---

## \* 사용했던 코딩

### 생성한 `device_user_id_summary` 테이블 파이썬으로 불러오기

```python

#  필요한 라이브러리 임포트

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus


#  MySQL 연결 정보 입력

user = '----'
password = '--'
host = '----'
port = 3306
database = 'final'

# 비밀번호 URL 인코딩 (특수문자 포함 대비)
password = quote_plus(password)

# SQLAlchemy 엔진 생성
engine = create_engine(
    f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
)


#  쿼리 실행 (데이터 가져오기)

query = """
SELECT *
FROM final.device_user_id_summary;
"""

# pandas로 데이터 전체 불러오기
df = pd.read_sql(query, con=engine)


#  기본 정보 출력

print("MySQL 연결 및 데이터 로드 성공!")
print(f"총 행 수: {len(df):,}")
print("컬럼 목록:", list(df.columns))
print("\n데이터 미리보기:")
display(df.head())

```

---

## \*문제점

- 기존 테이블에서 오류점을 발견하고, 구조를 재 정립하고, 개선하여 생성하기 까지 하루를 다 소모했다..

<BR>

## \* 회고

- user를 특정하였으니, 팀원들이 해당 데이터를 사용하여 같은 기준으로 분석한다면, 분석 결과끼리 스토리 잇기가 수월해질 것 같다
- 내일 바로 event_flow를 연결하여, 분석하고 진행해봐야겠다
