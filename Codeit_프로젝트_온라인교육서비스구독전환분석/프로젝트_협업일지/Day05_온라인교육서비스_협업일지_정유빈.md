# Day - 5 협업 일지(중급1)

#### 일자: 2025-07-11 / 정유빈

---

### 팀원들과 논의한 일

- 유저별 `complete.subscription` 로그 중복 발생 문제 공유
- `click.cancel_plan_button` 로그와의 시간 관계 검토 필요성 인식
- **정확한 구독 기간 산정을 위한 두 가지 분석 방식(PLAN A / PLAN B)** 설계 후 팀원들에게 공유, 비교 논의
- 분석 신뢰도 향상을 위해 **팀원 각자의 분석 방식 피드백 및 수정 방향 제안**

---

## \* 오늘 + 내가 한 일

- PLAN A / PLAN B 분석 전략 구조 설계 및 기준 정리

  - PLAN A: 첫 complete 이후 첫 cancel까지의 기간만 구독 기간으로 간주하는 보수적 방식
  - PLAN B: complete-cancel 반복 구간을 회차 단위로 구분하여 실제 전체 구독 기간을 합산

- 문제 인식: 일부 유저에서 `complete.subscription` 로그가 2회 이상 찍히며  
  기존의 단순 갯수 기반 LTR 계산이 과대 추정될 수 있음을 발견
- 해당 문제를 기반으로 팀원들과 논의
  - 현재 사용 중인 로그 테이블에서 발생 가능한 오류 공유
  - 팀원별 기존 분석 흐름에서 위 문제점으로 인해 발생할 문제들 피드백 및 수정 방향 제안

---

## \* 사용했던 코드

(아래에 코드 입력)

```python
# 1. complete(첫 결제 이력) 2회 이상 찍힌 유저 ID 목록
multi_complete_users = complete_counts[complete_counts['complete_subscription_count'] > 1]['user_id']

# 2. 유저별 최초 결제 시간
first_complete = (
    complete_df[complete_df['user_id'].isin(multi_complete_users)]
    .sort_values(by='client_event_time')
    .drop_duplicates(subset='user_id', keep='first')
    [['user_id', 'client_event_time']]
    .rename(columns={'client_event_time': 'first_complete_time'})
)

# 3. cancel 로그 준비
cancel_df['client_event_time'] = pd.to_datetime(cancel_df['client_event_time'])
filtered_cancel = cancel_df[cancel_df['user_id'].isin(multi_complete_users)]

# 4. cancel 로그와 최초 complete 시간 병합
cancel_merged = filtered_cancel.merge(first_complete, on='user_id', how='left')

# 5. 최초 결제 이후의 취소 로그만 필터링
cancel_after_first_payment = cancel_merged[
    cancel_merged['client_event_time'] >= cancel_merged['first_complete_time']
]

# 6. 유저별 취소 로그 개수 집계
cancel_counts = cancel_after_first_payment['user_id'].value_counts().reset_index()
cancel_counts.columns = ['user_id', 'cancel_count_after_first_payment']

# 상위 5명만 예시로 확인
cancel_counts
```

| user_id                          | cancel_count_after_first_payment |
| -------------------------------- | -------------------------------- |
| 42a0575943a53d5c9f9238c488b4fd33 | 4                                |
| 2fe40e7191a768e71edd18f11ab30e0c | 3                                |
| d8534b7743587af2f2989f4bbd5acf9e | 3                                |
| 10c43b95e86fd0feb871bd21bede50c6 | 3                                |
| 57d0d79f7f708d49bcb33e24d7ba1e78 | 3                                |
| ...                              | ...                              |
| c5087a941da4a7f8721fa4bc1923c253 | 1                                |
| d15c5972b231f1431c65a8ba44a92ed2 | 1                                |
| 433a7b7ae0c58e7badd304d9b0209e26 | 1                                |
| 92b37971a45e25d050ed996057c30746 | 1                                |
| ff990a16d0f5c8bf914a63b6815ed342 | 1                                |

<br>

---

<br>

## \* 문제점

- `complete.subscription` 로그가 유저별로 중복 기록되는 현상 확인됨  
  → 일부 유저는 최대 8회까지 결제 완료 로그가 존재함

- 기존 LTR 계산 방식(결제 횟수 기반)은 이 중복 로그로 인해 **구독 기간 및 매출 추정이 과대 계산될 가능성** 존재

- `click.cancel_plan_button` 로그 누락 문제가 있음  
  → 유저가 실제로 해지했더라도 **cancel 로그가 찍히지 않은 경우 다수 존재**  
  → 특히 `complete` 로그는 반복되는데 cancel 로그는 중간 회차에서 누락되는 경우도 있음  
  → 이로 인해 Plan B 방식(회차별 complete ↔ cancel 매칭 방식)은 **데이터 정합성 신뢰도가 낮아 적용 보류됨**
- 팀원들 각자의 기존 분석이 이 문제를 반영하지 못하고 있었음

---

## \* 회고

- 데이터를 충분이 확인하고 진행하였지만, 그래도 문제가 발생 → 더 꼼꼼히 생각하고 체크해야겠다를 실감했음

- PLAN A와 PLAN B의 장단점을 비교하며,  
  분석 목적과 데이터 신뢰도에 맞게 적절한 방식을 선택해야 함을 배움

- 팀 내 분석 기준이 달라 생길 수 있는 해석 차이를 방지하기 위해,  
  **초기 설계와 기준 공유의 중요성**을 실감한 하루였음
