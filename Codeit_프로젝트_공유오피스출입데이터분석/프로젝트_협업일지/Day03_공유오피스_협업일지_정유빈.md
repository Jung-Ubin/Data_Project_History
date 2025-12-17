# Day - 3 협업 일지(중급2)

#### 일자: 2025-09-08 / 정유빈

---

### 팀원들과 논의한 일

- f1-score 0.5 이상 나온 base-line 에서 FI(Feature_Importance) 확인
- 중요도가 높게 나온 컬럼 확인 후 각 팀원별 EDA 진행

## \* 오늘 + 내가 한 일

- EDA 진행

## \* 사용했던 코딩

- 각 유저들이 언느 시점에 결제를 많이 했는지(`start_trial_year` / `start_trial_month` 기준)

```python
# 연도-월별 결제율 계산
monthly_rate = (
    df.groupby(["start_trial_year", "start_trial_month"])["is_payment"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(12,6))
sns.barplot(
    x="start_trial_month",
    y="is_payment",
    hue="start_trial_year",
    data=monthly_rate,
    palette=["green", "blue", "yellow", "orange"]  # 초-파-노-주
)

plt.title("연도 & 월별 결제율")
plt.xlabel("월")
plt.ylabel("결제율")
plt.legend(title="연도")
plt.show()
```

---

## \*문제점

- EDA를 통해 "체험일수가 늘 수록 결제율이 올라간다." 란 특징 외 아직 발견한 점이 없음
- 팀원들과 EDA를 진행하고 있지만, 아직 다 갈피를 못잡는 느낌

## \* 회고

- 체험일수와 결제율 간의 상관관계를 확인했다. → 비즈니스 전략 방향성을 발견
- 데이터 수로 인해 착시가 올 수 있는 부분을 꼼꼼히 확인
- 하지만 얻은 인사이트가 한정적이고 구체적이지 못한 점이 아쉽다.
