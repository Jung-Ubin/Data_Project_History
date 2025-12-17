# Day - 12 협업 일지(고급)

#### 일자: 25-10-28 / 정유빈

---

### 팀원들과 논의한 일

- 각자 정한 분석 방향으로 분석 진행하면서 공유할 내용 있으면 공유하기

<br>

## \* 오늘 + 내가 한 일

### `device_user_id_summary` 테이블을 활용한 유저 이용 패턴 분석

- 본 테이블은 **`hackle_properties`**를 기반으로 생성되었으며, 데이터 수집 기간은 **2023년 7월 18일 ~ 8월 10일 (약 4주)**
- 한 달간의 데이터를 활용하면 `앱의 단기·반복 이용 패턴`을 구분할 수 있어, **유저의 지속 이용 여부를 파악하기에 적합하다고 판단**
- 이를 위해 각 유저가 보유한 **`session_id`의 개수(`session_count`)**를 중심으로 분석을 진행
- 세션 보유 수를 통해 **단발성 사용자 비율, 재방문 이용 패턴, 활성 사용자군의 특징을 파악**하고, 이후 **유입 유지율 개선을 위한 보완점을 도출하는 것이 목표**

<br>

#### `device_user_id_summary` 테이블 정보

| 구분                     | 내용                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **총 행 수**             | 228,205                                                                                                                                                      |
| **고유 `device_id` 수**  | 228,205                                                                                                                                                      |
| **고유 `user_id` 수**    | 228,205                                                                                                                                                      |
| **고유 `session_id` 수** | 228,390                                                                                                                                                      |
| **평균 `session_count`** | 약 1.0개 (2개 이상 보유 고유 `user_id` 수 : **186명**)                                                                                                       |
| **컬럼 구성**            | `num`, `device_id`, `user_id`, `osname`, `session_id`, `session_count`                                                                                       |
| **정제 기준**            | - 문자형·공란·NULL `user_id` 제거<br>- 여러 device를 거친 user 제거<br>- 여러 user를 거친 device 제거<br>- `(user_id, device_id, session_id)` 완전 중복 제거 |
| **데이터 특징**          | - user_id ↔ device_id **1:1 매핑 완성**<br>- 전체 사용자 중 약 **99% 이상 단일 세션 보유**<br>- 단기간(약 4주) 내 주로 **단발성 이용 패턴** 중심             |

---

### `session_count_1_log` : 단일 세션 보유 유저의 이벤트 흐름(테이블)

- `device_user_id_summary` 테이블 중 `session_count` = `1`인 유저를 선별  
  → 이들의 `session_id`를 `hackle_events` 테이블의 `session_id` 컬럼과 매칭

    <br>

- 이를 통해 각 유저의 단일 세션 내 **이벤트 발생 순서(`event_flow`)** 를 추출하고,  
  기존 컬럼(`device_id`, `user_id`, `osname`, `session_id`, `session_count`)에 `event_flow`를 추가한 **테이블(`session_count_1_log`)** 을 생성

    <br>

- 조건: 같은 행동이 연속적으로 반복되면 1개로 카운트한다. (ex: `A, B, C` = `3건` / `A, A, A, B, D, D, C` = `4건`)

    <br>

- 본 테이블은 **단일 세션 유저의 실제 이용 행동 흐름을 파악**하기 위한 기초 데이터로 활용

---

### `PrefixSpan` 사용하여 패턴 확인

- `evnet_count` 에서 이상치를 먼저 제거
- `PrefixSpan`을 활용해서 순차 패턴을 확인 (`min_support = 2` 로 설정)

---

### `PrefixSpan` 사용 시 문제 발생

- 해당 라이브러리 or 커스텀 클래스 사용 시 gcs가 끊기는 오류 발생함
- 해당 문제를 해결하고, 패턴을 찾아봐야 할 것 같음

---

## \* 사용했던 코딩

### `PrefixSpan` 라이브러리 사용했던 코

```python
from prefixspan import PrefixSpan

#  event_flow 문자열을 순서 리스트로 변환

# 콤마로 구분된 이벤트 시퀀스를 리스트로 변환
outlier_session_1_log_df['event_seq'] = outlier_session_1_log_df['event_flow'].apply(
    lambda x: [e.strip() for e in x.split(',') if e.strip() != '']
)

# 전체 시퀀스 데이터 구성
sequences = outlier_session_1_log_df['event_seq'].tolist()

print(f"총 {len(sequences)}개의 세션 시퀀스 로드 완료")
```

```python
# 해당 과정에서 gcs가 끊김 (데이터 규모가 약 22만행...인데 왜..) ####
# PrefixSpan 실행
ps = PrefixSpan(sequences)

# min_support=2 로 고정, 상위 50개 패턴 추출
patterns = ps.frequent(2)
patterns = sorted(patterns, key=lambda x: x[0], reverse=True)[:50]
```

```python

#  결과 정리 및 확인
pattern_df = pd.DataFrame(patterns, columns=['support', 'sequence'])
pattern_df['support_ratio'] = pattern_df['support'] / len(sequences)

print("\n===== PrefixSpan 결과 (min_support=2) =====")
pattern_df
```

---

## \*문제점

- 오늘도 분석 진도를 많이 나가질 못해 아쉽다.
- 오늘 개인 분석에서 문제점이 많아 수정하느라 팀원간 공유된 내용이 부족하여 내일은 팀원들과 이야기하고 분석 방향을 논의해볼 예정

<BR>

## \* 회고

- gcs 연결이 자꾸 끊겨서 손을 보느라 오늘 분석이 힘들었음
- 하지만 gcs를 수정해보는 과정에서, 앞으로 gcs가 끊겼을 때 대처하는 방법을 배웠음
- 그리고 `PrefixSpan` 이 방법을 사용하여 사용자의 순차 패턴을 뽑아보려했는데.. 다른 방법도 생각해봐야 할 것 같음..
