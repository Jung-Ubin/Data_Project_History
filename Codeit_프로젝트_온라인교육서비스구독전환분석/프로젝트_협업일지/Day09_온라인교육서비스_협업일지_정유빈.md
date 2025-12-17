# Day - 9 협업 일지(중급1)

#### 일자: 2025-07-17 / 정유빈

---

### 팀원들과 논의한 일

- 중간 보고서 작성 중 팀원 분석에서(리마인드 제안) 분석이 약간 틀어져 있는것을 확인
- 중간 보고서 마무리 후 대본 준비

---

## \* 오늘 + 내가 한 일

- 리마인드 전략 제안 분석에서 문제점을 발견하여,  
  해당 분석을 처음부터 다시 진행
- 각 무료 체험 기간 중, 무료 체험 사용 기간 종료 후 두 그룹으로 나눠서 구독 전환률 구한 후  
  각 그룹의 리마인드 메시지를 효율적으로 전달할 수 있는 기간을 추천

---

## \* 사용했던 코드

### 무료 체험 사용 이후 구독 전환률 확인 코드

```python
# 1. 8일차 이상 전환 유저 필터링
converted_after_7days = merged_with_free_trial[merged_with_free_trial['conversion_days'] > 7]

# 2. 일차별 전환 수 카운트
after_counts = converted_after_7days['conversion_days'].value_counts().sort_index()
after_cumsum = after_counts.cumsum()

# 3. 이상치: 음수거나 결측치
invalid_conversions = merged_with_free_trial[
    (merged_with_free_trial['conversion_days'].isna()) |
    (merged_with_free_trial['conversion_days'] < 0)
]
invalid_count = len(invalid_conversions)

# 4. 누적값 보정 (1735명은 1~7일차에서 전환한 유저 수)
base_cum = 1735
base_rate = 54.58  # 1~7일차 누적 전환율

# 5. DataFrame 만들기
side_result_df = pd.DataFrame({
    'conversion_day': after_counts.index,
    'daily_converted_users': after_counts.values,
    'cumulative_converted_users': after_cumsum.values + base_cum
})
side_result_df['cumulative_conversion_rate(%)'] = (
    side_result_df['cumulative_converted_users'] / total_trial_users * 100
).round(2)

# 6. 이상치 row 추가
outlier_row = pd.DataFrame({
    'conversion_day': ['이상치'],
    'daily_converted_users': [invalid_count],
    'cumulative_converted_users': [total_trial_users],
    'cumulative_conversion_rate(%)': [100.00]
})

# 7. 최종 연결
side_result_df = pd.concat([side_result_df, outlier_row], ignore_index=True)

# 결과 확인
print("무료 체험 이후 전환 분석 (8일차 이상 및 이상치 포함)")
display(side_result_df)
```

<br>

---

<br>

## \* 문제점

- 위 분석에서 하루 시간을 거의 소비하여, 중간 발표 자료 작성을 빠듯하게 진행함
- 팀원과 리허설을 진행해보려했지만, 시간이 부족하여 결국 진행하지 못하고 발표 자료만 마무리함

---

## \* 회고

- 같은 분석을 하는 팀원의 분석 과정을 듣지못하여, 잘못되고있는 과정중에 피드백을 하지 못하여 발생된 일
- 자주 팀원간 질문을 해가면서, 잘못된 부분은 없는지 바꿔야할 부분은 없는지 캐치하여 피드백하는 과정이 필요하다 느낌
