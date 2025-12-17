# Day - 7 협업 일지(중급1)

#### 일자: 2025-07-15 / 정유빈

---

### 팀원들과 논의한 일

- 각 팀원들 분석이 어떻게 이뤄지는지 인사이트 나올 때마다 서로 의견 및 인사이트 공유

---

## \* 오늘 + 내가 한 일

- 무료 체험 유저와 비 체험 유저의 평균 LTV 비교 분석 수행  
  → 각 유저의 LTR(Life-Time Revenue) 계산 후, 무료 체험자는 콘텐츠 사용량 기반 CAC를 반영하여 LTV 계산

- 레슨 1회당 수익 단가(760.27원)를 기준으로 무료 체험 1주일 평균 수강량(11.51건)을 곱해, 보수적인 CAC 추정값 8,751원 산출

- 위 CAC를 무료 체험 유저에게 적용하여 LTV 계산 후, 두 그룹 간 평균 LTV 비교  
  → 비 체험자 평균 LTV: **71,699원** / 무료 체험자 평균 LTV: **68,828원**

- 독립표본 t-test를 통해 평균 LTV 차이의 통계적 유의성 검정 수행  
  → p-value = 0.04558로 유의수준 0.05보다 작음 → 통계적으로 유의미한 차이로 판단

- 현재 LTV 차이는 무료 체험이 반드시 경제적 이득으로 이어지는 것은 아닐 수 있어 보여짐,  
  → 다만, 현재 CAC 추정이 "구독 유지 기간 기준 주당 수강량" 기반이라는 점에서(무료체험을 사용할 때로 안함),  
   내일은 무료 체험 기간 동안의 `enter.lesson_page` 의 `is_free_trial`을 기반으로 한 CAC 재추정이 필요하다고 판단됨

- 위 과정을 진행하고 결론/판단 하기 위한 데이터 프레임을 만들고 전처리 진행

---

## \* 사용했던 코드

### 구독 기간 내 레슨 완료 로그 몇 건씩 있는지

```python
# 1. 날짜 형식 변환
complete_lesson_df['client_event_time'] = pd.to_datetime(complete_lesson_df['client_event_time'])

# 2. 필요한 컬럼만 merge
merged = complete_lesson_df.merge(
    user_df_with_logs[['user_id', 'first_complete_time', 'subscription_end_date']],
    on='user_id',
    how='inner'
)

# 3. 기간 내 레슨 완료 로그 필터링
mask = (
    (merged['client_event_time'] >= merged['first_complete_time']) &
    (merged['client_event_time'] <= merged['subscription_end_date'])
)
filtered_logs = merged[mask]

# 4. 유저별 레슨 완료 수 세기
lesson_counts = filtered_logs.groupby('user_id').size().reset_index(name='lesson_complete_count_in_subscription')

# 5. 다시 user_df에 merge
user_df_with_logs = user_df_with_logs.merge(lesson_counts, on='user_id', how='left')

# 6. 레슨 수가 없는 유저는 0으로 처리
user_df_with_logs['lesson_complete_count_in_subscription'] = user_df_with_logs['lesson_complete_count_in_subscription'].fillna(0).astype(int)

# 7. 결과 확인
user_df_with_logs[['user_id', 'subscription_months', 'lesson_complete_count_in_subscription']]
```

<br>

---

<br>

## \* 문제점

- 무료 체험 유저의 CAC를 추정할 때, 실제 무료 체험 기간(7일) 중 소비한 콘텐츠 로그가 아닌,  
  **유료 구독 기간**의 **평균 주간 수강량을 기반으로 추정함**(차이없을거라고 추정하고진행했었음..)  
  → 이로 인해 실제보다 과도한 비용이 CAC로 계산되었을 가능성이 조금 보임

- 현재 LTV 분석은 무료 체험 기간의 실제 사용 로그를 반영하지 못하고 있음  
  → CAC가 부정확할 경우, 무료 체험의 경제적 효과를 과소평가할 수도 있을 것 같음  
  → 그래서 내일 그 부분만 기준(**`start.free_trial`로그 존재 유저 → `enter.lesson_page`내 `is_free_trial`컬럼 True값 유저**)  
   을 다시 설정하여, 새 (enter)CAC, (enter)LTV 컬럼을 기존 CAC, LTV 컬럼 옆에 두고 서로 비교해 볼 예정

---

## \* 회고

- 오늘 분석을 통해 무료 체험의 전환률 효과 외에도,  
  실제 수익 기여도(LTV) 측면에서의 경제적 타당성을 정량적으로 검증해볼 수 있었다는 점에서 의미 있었음

- 다만, CAC를 추정하는 방식의 정교함이 최종 LTV 비교에 큰 영향을 준다는 점도 체감하게 되었음  
  → 분석 흐름 자체는 탄탄했지만, 다음엔 **보다 정확한 사용자 행동 데이터 기반 CAC 추정**이 중요하다고 느꼈음

- 전환률이 높다고 해서 곧바로 수익성으로 이어지는 것은 아니라는 점에서,  
  **무료 체험 정책을 적용할 것인지, 어떤 유저군에 선별 적용할 것인지** 판단 기준도 함께 고민할 필요가 있다고 느꼈음
