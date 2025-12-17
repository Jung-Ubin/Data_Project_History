# Day - 11 협업 일지(중급1)

#### 일자: 2025-07-21 / 정유빈

---

### 팀원들과 논의한 일

- 최종 보고서를 어떤식으로 작성할건지에 대해서 팀원간 의견 제시
- 각 팀원들의 인사이트 다시 정리
- 최종 보고서 초안 작성 관련 진행 방법 논의

---

## \* 오늘 + 내가 한 일

- 저번주에 결론 났던 인사이트 "무료 체험자의 전환률은 비 체험자보다 3배 이상 높지만 경제적인 이득으로는 손해"
- 해당 인사이트를 활용하여 새로운 분석인 "무료 체험 기간 vs 무료 체험 폐지 기간의 lesson 소비량 비교" 분석 진행
- 위 분석을 통해 무료 체험 기간이 lesson 소비량이 더 높이 나와서 해당 인사이트로
- "무료 체험 시 구독 전환률이 약 3배 높아지며, 각 컨텐츠 소비량도 높아져서 전환률 자체에 효과가 있다."
- "하지만, LTV는 낮기 때문에 무료 체험 서비스의 LTV 관련 개선을 하여 개편 후 활용" 하자는 제안 아이템 생성
- 분석들 인사이트를 가지고 최종 보고서 작성 진행

---

## \* 사용했던 코드

### 무료 체험 기간 vs 무료 체험 폐지 기간의 lesson 소비량 비교

```python
# 1. 필요한 컬럼만 추출
df = complete_lesson_df[['user_id', 'lesson_complete_time', 'lesson.id']].copy()

# 2. 날짜 필터링
group_a_df = df[(df['lesson_complete_time'] >= '2023-01-01') & (df['lesson_complete_time'] <= '2023-02-28')]
group_b_df = df[(df['lesson_complete_time'] >= '2023-06-01') & (df['lesson_complete_time'] <= '2023-07-31')]

# 3. 유저별 고유 레슨 수 계산 (중복 lesson.id 제거)
group_a_unique_lessons = group_a_df.drop_duplicates(subset=['user_id', 'lesson.id']) \
                                   .groupby('user_id')['lesson.id'].count().reset_index(name='unique_lessons')
group_b_unique_lessons = group_b_df.drop_duplicates(subset=['user_id', 'lesson.id']) \
                                   .groupby('user_id')['lesson.id'].count().reset_index(name='unique_lessons')

# 4. 각 그룹의 평균 고유 레슨 수 계산
group_a_avg = group_a_unique_lessons['unique_lessons'].mean()
group_b_avg = group_b_unique_lessons['unique_lessons'].mean()

print(f"그룹 A (1~2월) 평균 고유 레슨 수: {group_a_avg:.2f}")
print(f"그룹 B (6~7월) 평균 고유 레슨 수: {group_b_avg:.2f}")

```

<BR>

그룹 A (1~2월) 평균 고유 레슨 수: 83.18  
그룹 B (6~7월) 평균 고유 레슨 수: 49.41

<br>

---

<br>

## \* 문제점

- 리마인드 전략 배치 아이템과, 위 설명한 아이템 2개를 제안서에 포함시킬 예정이고, 이걸 어떻게  
  보고서에 설득력있게 작성할 수 있을지 고민 중에 있음
- 각 팀원들의 보고서 작성 후 서식과 내용 맟추기 및 발표 자료까지 만드려면 시간이 촉박하다고 느껴짐

---

## \* 회고

- 일단 지금까지 분석한 내용들을 중간 보고서 때 작성한 경험을 살려서 깔끔하게 작성하는 것을 목표로 삼음
- 오늘은 소통을 별로 하지못하여, 서식과 시각화 작업 초안이 조금 다르게 나와서,  
  내일 같은 분석을 한 팀원과 계속 소통을 하면서 보고서 작성을 진행해야 겠다고 느낌
