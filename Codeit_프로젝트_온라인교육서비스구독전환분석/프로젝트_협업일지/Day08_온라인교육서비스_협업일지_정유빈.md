# Day - 8 협업 일지(중급1)

#### 일자: 2025-07-16 / 정유빈

---

### 팀원들과 논의한 일

- 각 분석 분야에서 중간 보고서 작성하는 인원들 중 한 명씩 뽑아서, 중간 보고서 작성 진행

---

## \* 오늘 + 내가 한 일

- 중간 보고서 작성 진행
- 분석한 부분이 많아서, 생각한 과정과 이 분석으로 어떤 인사이트를 얻고 추가적인 분석을 진행할 것인지 위주로 작성

---

## \* 사용했던 코드

### IQR 활용하여 이상치 파악

```python
Q1 = filtered_df['lesson_complete_count_in_subscription'].quantile(0.25)
Q3 = filtered_df['lesson_complete_count_in_subscription'].quantile(0.75)
IQR = Q3 - Q1

upper_1_5 = Q3 + 1.5 * IQR
upper_3_0 = Q3 + 3.0 * IQR

outlier_1_5_count = (filtered_df['lesson_complete_count_in_subscription'] > upper_1_5).sum()
outlier_3_0_count = (filtered_df['lesson_complete_count_in_subscription'] > upper_3_0).sum()

print(f"Q1: {Q1}")
print(f"Q3: {Q3}")
print(f"IQR: {IQR}")
print(f"\n[1.5 IQR 초과] 상한: {upper_1_5:.2f} → 유저 수: {outlier_1_5_count}")
print(f"[3.0 IQR 초과] 상한: {upper_3_0:.2f} → 유저 수: {outlier_3_0_count}")
```

Q1: 29.0  
Q3: 170.0  
IQR: 141.0

[1.5 IQR 초과] 상한: 381.50 → 유저 수: 993  
[3.0 IQR 초과] 상한: 593.00 → 유저 수: 379

<br>

---

<br>

## \* 문제점

- 최대한 다른 팀들과 인사이트를 공유하므로서 부트캠프 인원 전체적으로 퀄리티가 올라갈 수 있도록 작업 진행을 했으나,
- 시간이 그만큼 오래걸렸으며, 발표 대본 준비를 늦어 결국 발표 리허설을 팀원들이랑 못해봄.

---

## \* 회고

- 내일 중간 발표 자료를 마무리하여, 발표 리허설까지 마무리할 수 있도록 속도를 내야겠다.
- 최종 보고서 작성 시 오늘 작성했을 때 경험을 바탕으로 수월하게 작성할 수 있도록 부족한 점 보완.
