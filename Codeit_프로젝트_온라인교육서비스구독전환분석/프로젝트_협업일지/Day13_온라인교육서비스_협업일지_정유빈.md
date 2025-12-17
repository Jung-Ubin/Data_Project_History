# Day - 13 협업 일지(중급1)

#### 일자: 2025-07-23 / 정유빈

---

### 팀원들과 논의한 일

- 어제 이어서 최종 보고서 작성 및 의견 공유

---

## \* 오늘 + 내가 한 일

- 최종 보고서 작성 및 전체 보고서 서식 정리
- 보고서를 바탕으로 발표 자료 제작
- 리마인드 전략 분석 재 분석하여 더 정확한 인사이트 확보
- 분석 3 액션 아이템 수정

---

## \* 사용했던 코드

### 무료 체험 구독자들의 체험 시작 기준 일차별 누적 전환률 분포 파악

```python
# 전체 3162명 기준
total_users = merged_users_kr.shape[0]

# 구독까지 걸린 일수 분포
days_counts = merged_users_kr['구독까지 걸린 일수'].value_counts().sort_index()

# 누적 합
cumulative_counts = days_counts.cumsum()

# 누적 전환율 계산 (%)
cumulative_rate = cumulative_counts / total_users * 100

# DataFrame으로 정리
conversion_curve = pd.DataFrame({
    '일수': cumulative_rate.index,
    '누적 전환자 수': cumulative_counts.values,
    '누적 전환율(%)': cumulative_rate.values
})
```

<br>

---

<br>

## \* 문제점

- 분석 3 에서의 인사이트가 비슷한 내용으로 분석한 4팀과 달라서 재 분석 진행  
  → 결과가 크게 바뀌진 않았지만 다음부턴 신경써서 진행해야겠다.
- 1-1팀의 보고서가 아직 작성이 안되서 서식 정리를 못하는 이슈 발생  
  → 작성완료 되기 전까지 발표자료 분량을 어서 끝내고 서식 관리를 해야할 것 같음

---

## \* 회고

- 분석 할 때 최대한 더 꼼꼼히 분석에서 놓치는 부분이 없는지 생각하면서 해야겠다.
- 최종 보고서의 퀄리티를 최대한 높여서 **'결정을 하게 만들고 싶은'** 보고서로 만들어보자.
